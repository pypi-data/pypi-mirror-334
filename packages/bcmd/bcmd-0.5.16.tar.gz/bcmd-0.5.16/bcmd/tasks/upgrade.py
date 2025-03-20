from typing import Final

import pyperclip
from beni import bcolor, btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def upgrade():
    '使用 pipx 官方源更新 bcmd 到最新版本'
    cmd = 'pipx upgrade bcmd -i https://pypi.org/simple'
    pyperclip.copy(cmd + '\n')
    bcolor.printGreen(cmd)
    bcolor.printGreen('已复制到剪贴板（需要手动执行）')
    bcolor.printGreen('OK')
