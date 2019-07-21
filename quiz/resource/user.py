from flask import current_app

from quiz.task.email import send_async_reg_email
from quiz.model.query import user as user_api
from quiz.exceptions import ValidateException


def user_register(username, email, password):
    """用户注册"""

    # 验证用户名和邮箱的唯一性
    if user_api.user_first(username=username):
        raise ValidateException('Please use a different username')

    if user_api.user_first(email=email):
        raise ValidateException('Please use a different email')

    user = user_api.user_create(username=username, email=email, password=password)

    token = user.generate_confirm_jwt()

    _send_confirm_email(email, token)

    return user


def resend_confirm_email(email):
    """重新发送注册邮件"""
    user = user_api.user_first(email=email)
    if not user:
        raise ValidateException('邮箱不存在或者尚未注册')

    token = user.generate_confirm_jwt()

    _send_confirm_email(email, token)


def _send_confirm_email(email, token):
    send_async_reg_email.delay('[Quiz] Confirm Your Account',
                               current_app.config['MAIL_DEFAULT_SENDER'],
                               [email],
                               token)

