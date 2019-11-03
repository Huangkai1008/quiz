import datetime as dt
import decimal
import json
import enum
from collections.abc import Iterator

from quiz.model.base import ModelMixin


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
        elif isinstance(o, ModelMixin):
            return dict(o)
        elif isinstance(o, enum.Enum):
            return o.value
        return json.JSONEncoder.default(self, o)


class Singleton(type):
    """
    单例
    """

    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def paginate(results: list, page=1, size=10):
    """
    分页
    :param results:
    :param page
    :param size
    :return:
    """
    return results[(page - 1) * size : size + (page - 1) * size]
