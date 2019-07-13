import datetime as dt
import decimal
import json
from collections import Iterator

import jwt


class ExtendedEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, dt.date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, decimal.Decimal):
            return int(o)
        elif isinstance(o, Iterator):
            return list(o)
        return json.JSONEncoder.default(self, o)


class Jwt:
    """
    jwt 工具类
    """

    def __init__(self, secret_key):
        self._secret_key = secret_key

    def generate_confirm_jwt(self, user_id):
        """生成确认账户的Jwt"""
        now = dt.datetime.utcnow()

        payload = dict(
            confirm=user_id,
            exp=now + dt.timedelta(seconds=60 * 60),
            iat=now,
            aud='quiz'
        )

        token = jwt.encode(payload, self._secret_key, 'HS256').decode('utf-8')
        return token
