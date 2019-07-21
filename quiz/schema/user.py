from quiz.schema.base import Schema
from quiz.schema.schemas import UserSchemas


class RegisterSchema(Schema):
    """
    注册
    """
    _schema = UserSchemas.REG_SCHEMA.value


class LoginSchema(Schema):
    """
    登录
    """
    _schema = UserSchemas.LOGIN_SCHEMA.value
