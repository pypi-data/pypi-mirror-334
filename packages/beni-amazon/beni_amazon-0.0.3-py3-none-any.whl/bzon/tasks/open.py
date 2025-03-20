from __future__ import annotations

import webbrowser
from typing import Final

import pyperclip
import typer
from beni import btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def open(
    asin_list: list[str] = typer.Argument(None, help='ASIN 列表'),
):
    '打开 Amazon 商品页面，可以使用参数指定 asin 或将 asin 列表复制到剪贴板'
    if not asin_list:
        asin_list = pyperclip.paste().strip().split(' ')
        asin_list = [x.strip() for x in asin_list]
        asin_list = [x for x in asin_list if x]
    assert asin_list, 'ASIN 列表不能为空'
    for asin in asin_list:
        webbrowser.open(f'https://www.amazon.com/dp/{asin}')
