from flask import render_template, current_app
from flask_mail import Message

from quiz.task import celery
from quiz.extensions import mail


@celery.task
def send_async_reg_email(subject, sender, recipients, token):
    """
    发送注册激活邮件
    :param subject 主题
    :param sender 发送者
    :param recipients 接收者 []
    :param token  jwt-token
    :return:
    """
    message = Message(subject=subject, sender=sender, recipients=recipients)

    message.html = render_template(
        'send_reg_email.html',
        confirm_url=f"{current_app.config['CONFIRM_EMAIL_URL']}/{token}",
    )

    mail.send(message)
