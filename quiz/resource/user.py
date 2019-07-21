from flask import current_app

from quiz import utils
from quiz.task.email import send_async_reg_email
from quiz.model.query import user as user_api
from quiz.exceptions import ValidateException


class UserResource(metaclass=utils.Singleton):
    """
    用户
    """

    @staticmethod
    def user_register(username, email, password):
        """用户注册"""

        # 验证用户名和邮箱的唯一性
        if user_api.user_first(username=username):
            raise ValidateException('Please use a different username')

        if user_api.user_first(email=email):
            raise ValidateException('Please use a different email')

        user = user_api.user_create(username=username, email=email, password=password)

        token = user.generate_confirm_jwt()

        send_async_reg_email.delay('[Quiz] Confirm Your Account',
                                   current_app.config['MAIL_DEFAULT_SENDER'],
                                   [email],
                                   token)

        return user


user_resource = UserResource()
