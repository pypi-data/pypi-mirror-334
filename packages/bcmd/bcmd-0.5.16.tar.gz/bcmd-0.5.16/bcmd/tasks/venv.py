import os
import platform
import re
import sys
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bexecute, bfile, bhttp, bpath, brun, btask
from beni.bfunc import syncCall
from beni.btype import Null
from prettytable import PrettyTable

from ..common.func import checkFileOrNotExists, checkPathOrNotExists

app: Final = btask.newSubApp('venv 相关')


@app.command()
@syncCall
async def add(
    packages: list[str] = typer.Argument(None),
    path: Path = typer.Option(None, '--path', help='指定路径，默认当前目录'),
    isOfficial: bool = typer.Option(False, '--official', help='是否使用官方地址安装（https://pypi.org/simple）'),
):
    '添加指定库'
    await _venv(
        packages,
        path=path,
        isOfficial=isOfficial,
    )


@app.command()
@syncCall
async def install_benimang(
    path: Path = typer.Option(None, '--path', help='指定路径，默认当前目录'),
):
    '更新 benimang 库，强制使用官方源'
    path = path or Path(os.getcwd())
    pip = getPipFile(path)
    await brun.run(f'{pip} install benimang -U -i https://pypi.org/simple', isPrint=True)
    await _venv(
        ['benimang==now'],
        path=path,
    )


@app.command()
@syncCall
async def install_base(
    path: Path = typer.Option(None, '--path', help='指定路径，默认当前目录'),
    isOfficial: bool = typer.Option(False, '--official', help='是否使用官方地址安装（https://pypi.org/simple）'),
    isReinstall: bool = typer.Option(False, '--reinstall', help='是否清空venv目录后重新安装'),
):
    '安装基础库'
    await _venv(
        path=path,
        isOfficial=isOfficial,
        isUseBase=True,
        isCleanup=isReinstall,
    )


@app.command()
@syncCall
async def install_lock(
    path: Path = typer.Option(None, '--path', help='指定路径，默认当前目录'),
    isOfficial: bool = typer.Option(False, '--official', help='是否使用官方地址安装（https://pypi.org/simple）'),
    isReinstall: bool = typer.Option(False, '--reinstall', help='是否清空venv目录后重新安装'),
):
    '安装指定版本的库'
    await _venv(
        path=path,
        isOfficial=isOfficial,
        isUseLock=True,
        isCleanup=isReinstall,
    )


# ------------------------------------------------------------------------------------

async def _venv(
    packages: list[str] = [],
    *,
    path: Path = Null,
    isOfficial: bool = False,
    isUseBase: bool = False,
    isUseLock: bool = False,
    isCleanup: bool = False,
):
    'python 虚拟环境配置'
    btask.assertTrue(not (isUseBase == isUseLock == True), '2个选项只能选择其中一个 --use-base / --use-lock')
    path = path or Path(os.getcwd())
    venvPath = getVenvPath(path)
    checkPathOrNotExists(venvPath)
    venvFile = bpath.get(path, '.venv')
    checkFileOrNotExists(venvFile)
    if isCleanup:
        bpath.remove(venvPath)
        btask.assertTrue(not venvPath.exists(), f'无法删除 venv 目录 {venvPath}')
    packages = packages or []
    for i in range(len(packages)):
        package = packages[i]
        if package.endswith('==now'):
            ary = package.split('==')
            packages[i] = f'{ary[0]}=={await _getPackageLatestVersion(ary[0])}'
    if not venvPath.exists():
        await bexecute.run(f'python -m venv {venvPath}')
    if not venvFile.exists():
        await bfile.writeText(venvFile, '')
    basePackages, lockPackages = await getPackageList(venvFile)
    if isUseBase:
        installPackages = _mergePackageList(basePackages, packages)
    elif isUseLock:
        installPackages = _mergePackageList(lockPackages, packages)
    else:
        installPackages = _mergePackageList(lockPackages or basePackages, packages)
    installPackages = sorted(list(set(installPackages)))
    pip = getPipFile(path)
    await _pipInstall(pip, installPackages, isOfficial)
    with bpath.useTempFile() as tempFile:
        await bexecute.run(f'{pip} freeze > {tempFile}')
        basePackages = _mergePackageList(basePackages, packages)
        lockPackages = (await bfile.readText(tempFile)).replace('\r\n', '\n').strip().split('\n')
        await updatePackageList(venvFile, basePackages, lockPackages)
    bcolor.printGreen('OK')


async def _pipInstall(pip: Path, installPackages: list[str], disabled_mirror: bool):
    python = pip.with_stem('python')
    btask.assertTrue(python.is_file(), f'无法找到指定文件 {python}')
    btask.assertTrue(pip.is_file(), f'无法找到指定文件 {pip}')
    indexUrl = '-i https://pypi.org/simple' if disabled_mirror else ''
    with bpath.useTempFile() as file:
        await bfile.writeText(file, '\n'.join(installPackages))
        table = PrettyTable()
        table.add_column(
            bcolor.yellow('#'),
            [x + 1 for x in range(len(installPackages))],
        )
        table.add_column(
            bcolor.yellow('安装库'),
            [x for x in installPackages],
            'l',
        )
        print(table.get_string())

        btask.assertTrue(
            not await bexecute.run(f'{python} -m pip install --upgrade pip {indexUrl}'),
            '更新 pip 失败',
        )
        btask.assertTrue(
            not await bexecute.run(f'{pip} install -r {file} {indexUrl}'),
            '执行失败',
        )


async def _getPackageDict(venvFile: Path):
    content = await bfile.readText(venvFile)
    pattern = r'\[\[ (.*?) \]\]\n(.*?)(?=\n\[\[|\Z)'
    matches: list[tuple[str, str]] = re.findall(pattern, content.strip(), re.DOTALL)
    return {match[0]: [line.strip() for line in match[1].strip().split('\n') if line.strip()] for match in matches}


_baseName: Final[str] = 'venv'


def _getLockName():
    systemName = platform.system()
    return f'{_baseName}-{systemName}'


async def getPackageList(venvFile: Path):
    result = await _getPackageDict(venvFile)
    lockName = _getLockName()
    return result.get(_baseName, []), result.get(lockName, [])


async def updatePackageList(venvFile: Path, packages: list[str], lockPackages: list[str]):
    packageDict = await _getPackageDict(venvFile)
    lockName = _getLockName()
    packages.sort(key=lambda x: x.lower())
    lockPackages.sort(key=lambda x: x.lower())
    packageDict[_baseName] = packages
    packageDict[lockName] = lockPackages
    content = '\n\n\n'.join([f'\n[[ {key} ]]\n{'\n'.join(value)}' for key, value in packageDict.items()]).strip()
    await bfile.writeText(venvFile, content)


async def _getPackageLatestVersion(package: str):
    '获取指定包的最新版本'
    data = await bhttp.getJson(
        f'https://pypi.org/pypi/{package}/json'
    )
    return data['info']['version']


def _mergePackageList(basePackages: list[str], addPackages: list[str]):
    basePackagesDict = {_getPackageName(x): x for x in basePackages}
    addPackagesDict = {_getPackageName(x): x for x in addPackages}
    packagesDict = basePackagesDict | addPackagesDict
    return sorted([x for x in packagesDict.values()])


def _getPackageName(package: str):
    if '==' in package:
        package = package.split('==')[0]
    elif '>' in package:
        package = package.split('>')[0]
    elif '<' in package:
        package = package.split('<')[0]
    package = package.strip()
    if package.startswith('#'):
        package = package.replace('#', '', 1).strip()
    return package


def getVenvPath(path: Path):
    return bpath.get(path, 'venv')


def getPipFile(path: Path):
    if sys.platform.startswith('win'):
        return bpath.get(getVenvPath(path), 'Scripts/pip.exe')
    else:
        return bpath.get(getVenvPath(path), 'bin/pip')
