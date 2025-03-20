from __future__ import annotations

from typing import Final

from beni import btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def hello():
    print('hello')


@app.command()
@syncCall
async def bye():
    print('bye')
