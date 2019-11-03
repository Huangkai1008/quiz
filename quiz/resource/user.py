from flask import current_app, g

from quiz.task.email import send_async_reg_email
from quiz.model.queries import user as user_api
from quiz.exceptions import ValidateException


def user_register(username, email, password):
    """用户注册"""

    # 验证用户名和邮箱的唯一性
    if user_api.get_user(username=username):
        raise ValidateException('Please use a different username')

    if user_api.get_user(email=email):
        raise ValidateException('Please use a different email')

    user = user_api.create_user(username=username, email=email, password=password)

    token = user.generate_confirm_jwt()

    _send_confirm_email(email, token)

    return user


def resend_confirm_email(email):
    """重新发送注册邮件"""
    user = user_api.get_user(email=email)
    if not user:
        raise ValidateException('邮箱不存在或者尚未注册')

    token = user.generate_confirm_jwt()

    _send_confirm_email(email, token)


def _send_confirm_email(email, token):
    send_async_reg_email.delay(
        '[Quiz] Confirm Your Account',
        current_app.config['MAIL_DEFAULT_SENDER'],
        [email],
        token,
    )


def get_followed():
    """获取用户关注的所有用户"""
    follower_id = g.current_user.id

    followed_ids = [
        follower.followed_id for follower in user_api.get_followed(follower_id)
    ]
    users = user_api.get_users(user_ids=followed_ids)
    return users


def follow_user(user_id):
    """关注用户"""
    follower = g.current_user
    followed_person = user_api.get_user(user_id=user_id)
    if follower == followed_person:
        raise ValidateException('你不能关注自己')

    if user_api.exist_follow(follower.id, user_id):
        raise ValidateException('你已经关注了此用户')
    else:
        user_api.create_follow(follower.id, user_id)
