from pathlib import Path
from typing import Final

import typer
from beni import bcolor, binput, bpath, brun, btask
from beni.bfunc import syncCall

from ..common.func import useResources
from . import venv

app: Final = btask.newSubApp('项目相关')


@app.command()
@syncCall
async def create_py(
    path: Path = typer.Option(Path.cwd(), '--path', help='workspace 路径'),
):
    '生成新项目'

    # 检查目标路径是否合法
    if path.exists():
        if not path.is_dir():
            bcolor.printRed('目标路径不是一个目录', path)
            return
        elif list(bpath.get(path).glob('*')):
            bcolor.printRed('目标路径不是空目录', path)
            return

    bcolor.printYellow(path)
    await binput.confirm('即将在此路径生成新项目，是否继续？')
    venv.add(['benimang==now'], path)
    with useResources('project') as sourceProjectPath:
        bpath.copyOverwrite(sourceProjectPath, path)


@app.command()
@syncCall
async def install(
    path: Path = typer.Option(Path.cwd(), '--path', help='初始化项目的路径'),
    deep: int = typer.Option(3, '--deep', help='探索路径深度（默认：1）'),
):
    '初始化项目（python项目执行beni venv install-lock / nodejs项目执行 pnpm install）'

    async def checkPath(currentPath: Path, currentDeep: int):
        for file in bpath.listFile(currentPath):
            if file.name == '.venv':
                with bpath.changePath(file.parent):
                    await brun.run('beni venv install-lock', isPrint=True)
                return
            elif file.name == 'package.json':
                with bpath.changePath(file.parent):
                    await brun.run('pnpm install', isPrint=True)
                return
        if currentDeep < deep:
            for folder in bpath.listPath(currentPath):
                await checkPath(folder, currentDeep + 1)

    await checkPath(path, 0)
