import getpass
from typing import Any

from beni import bcache, bcrypto


@bcache.cache
async def getQiniu() -> tuple[str, str]:
    content = '7xOuA0FPCndTWcWmWLbqklQTqLTAhuEw9CarRTBYhWQ/g8wPxktw6VAiu50TLv49D1L8oCVfGafsowYDZw/prF6NQwCluPcCMy5JfdC9sKauvuZa51Nsf6PTR1UIyU8ZLUSzH+Ec2Ufcz/yAZCrcAtn63zMHNu3tTAVcZNPL597lSHdSRkpmDR8CaoUh/raH/Q=='
    data = _getData(content)
    return data['ak'], data['sk']


def _getData(content: str) -> dict[str, Any]:
    index = content.find(' ')
    if index > -1:
        tips = f'请输入密码（{content[:index]}）：'
    else:
        tips = '请输入密码：'
    while True:
        try:
            pwd = getpass.getpass(tips)
            return bcrypto.decryptJson(content, pwd)
        except KeyboardInterrupt:
            raise Exception('操作取消')
        except BaseException:
            pass
