import datetime as dt
import decimal
import json
from collections import Iterator


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