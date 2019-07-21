# -*- coding:utf-8 -*-
"""
自定义异常
"""


class QuizException(Exception):
    """
    前端参数异常
    """
    status_code = 400

    def __init__(self, message):
        super(QuizException, self).__init__(message)
        self.message = message

    def __iter__(self):
        for k in ['message', 'status_code']:
            yield (k, getattr(self, k))


class AuthException(Exception):
    """
    权限异常
    """
    status_code = 401

    def __init__(self, message):
        super(AuthException, self).__init__(message)
        self.message = message

    def __iter__(self):
        for k in ['message', 'status_code']:
            yield (k, getattr(self, k))


class NotFoundException(Exception):
    """
    Not Found异常
    """
    status_code = 404

    def __init__(self, message):
        super(NotFoundException, self).__init__(message)
        self.message = message

    def __iter__(self):
        for k in ['message', 'status_code']:
            yield (k, getattr(self, k))


class ServerException(Exception):
    """
    服务器内部错误
    """
    status_code = 500

    def __init__(self, message):
        super(ServerException, self).__init__(message)
        self.message = message

    def __iter__(self):
        for k in ['message', 'status_code']:
            yield (k, getattr(self, k))


class ValidateException(QuizException):
    """
    验证json数据错误
    """
    pass
