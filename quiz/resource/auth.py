from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from quiz.model.user import User
from quiz.exceptions import AuthException

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')


@token_auth.verify_token
def verify_token(token):
    """验证用户请求中是否有token而且token存在并且未过期 """
    g.current_user = User.verify_jwt(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    """token auth验证失败"""
    raise AuthException('Token Auth verify failed')
