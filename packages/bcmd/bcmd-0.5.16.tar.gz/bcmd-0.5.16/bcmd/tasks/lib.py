import os
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bfile, bpath, btask
from beni.bfunc import syncCall, textToAry

from ..common import password
from .venv import getPackageList

app: Final = btask.newSubApp('lib 工具')


@app.command()
@syncCall
async def tidy_dependencies(
    workspace_path: Path = typer.Argument(Path.cwd(), help='workspace 路径'),
    isWithVersion: bool = typer.Option(False, '--with-version', help='是否带版本号')
):
    '整理 pyproject.toml 里面的 dependencies'
    pyprojectTomlFile = workspace_path / 'pyproject.toml'
    btask.assertTrue(pyprojectTomlFile.is_file(), 'pyproject.toml 不存在', pyprojectTomlFile)
    venvFile = bpath.get(workspace_path, f'.venv')
    btask.assertTrue(venvFile.is_file(), '.venv 不存在', venvFile)
    basePackages, lockPackages = await getPackageList(venvFile)
    libAry = lockPackages if isWithVersion else basePackages
    oldContent = await bfile.readText(pyprojectTomlFile)
    ignoreLibAry = _getIgnoreLibAry(oldContent)
    ignoreLibAry = sorted(list(set(ignoreLibAry) & set(libAry)))
    libAry = sorted(list(set(libAry) - set(ignoreLibAry)))
    replaceContent = '\n'.join([f"  '{x}'," for x in libAry]) + '\n' + '\n'.join([f"  # '{x}'," for x in ignoreLibAry])
    newContent = re.sub(r'dependencies = \[(.*?)\n\]', f"dependencies = [\n{replaceContent}\n]", oldContent, 0, re.DOTALL)
    if oldContent != newContent:
        await bfile.writeText(pyprojectTomlFile, newContent)
        bcolor.printYellow(pyprojectTomlFile)
        bcolor.printMagenta(newContent)
        return True
    else:
        bcolor.printGreen('无需修改依赖')
        return False


@app.command()
@syncCall
async def update_version(
    path: Path = typer.Argument(Path.cwd(), help='workspace 路径'),
    isNotCommit: bool = typer.Option(False, '--no-commit', '-d', help='是否提交git'),
):
    '修改 pyproject.toml 版本号'
    file = path / 'pyproject.toml'
    btask.assertTrue(file.is_file(), '文件不存在', file)
    data = await bfile.readToml(file)
    version = data['project']['version']
    versionList = [int(x) for x in version.split('.')]
    versionList[-1] += 1
    newVersion = '.'.join([str(x) for x in versionList])
    content = await bfile.readText(file)
    if f"version = '{version}'" in content:
        content = content.replace(f"version = '{version}'", f"version = '{newVersion}'")
    elif f'version = "{version}"' in content:
        content = content.replace(f'version = "{version}"', f'version = "{newVersion}"')
    else:
        raise Exception('版本号修改失败，先检查文件中定义的版本号格式是否正常')
    await bfile.writeText(file, content)
    bcolor.printCyan(newVersion)
    if not isNotCommit:
        msg = f'更新版本号 {newVersion}'
        os.system(
            rf'TortoiseGitProc.exe /command:commit /path:{file} /logmsg:"{msg}"'
        )
    bcolor.printGreen('OK')


@app.command()
@syncCall
async def build(
    path: Path = typer.Argument(Path.cwd(), help='workspace 路径'),
    isKeepBuildFiles: bool = typer.Option(False, '--keep-build-files', '-k', help='是否保留构建文件'),
):
    '发布项目'
    u, p = await password.getPypi()
    with _useBuildPath(path, isKeepBuildFiles):
        scriptPath = (path / './venv/Scripts')
        os.system(f'{scriptPath / "python.exe"} -m build')
        os.system(f'{scriptPath / "twine.exe"} upload dist/* -u {u} -p {p}')


# ------------------------------------------------------------------------------------


def _getIgnoreLibAry(content: str) -> list[str]:
    '获取pyproject.toml中屏蔽的第三方库'
    content = re.findall(r'dependencies = \[(.*?)\n\]', content, re.DOTALL)[0]
    ary = textToAry(content)
    return sorted([x[1:].replace('"', '').replace("'", '').replace(',', '').strip() for x in filter(lambda x: x.startswith('#'), ary)])


@contextmanager
def _useBuildPath(workspacePath: Path, isKeepBuildFiles: bool):
    '整理构建目录，先清空不必要的输出目录，结束后再判断是否需要再清空一次'

    def removeUnusedPath():
        bpath.remove(workspacePath / 'dist')
        paths = bpath.listDir(workspacePath)
        for x in paths:
            if x.name.endswith('.egg-info'):
                bpath.remove(x)

    try:
        with bpath.changePath(workspacePath):
            removeUnusedPath()
            yield
    finally:
        if not isKeepBuildFiles:
            removeUnusedPath()
