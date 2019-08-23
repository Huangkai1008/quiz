import datetime as dt

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from quiz.model.base import Model
from quiz.extensions import db

__all__ = ['User']


class User(Model):
    """
    用户模块
    """
    _hide_columns = {'password'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False, comment='用户名')
    email = db.Column(db.String(128), unique=True, nullable=False, comment='邮箱')
    password = db.Column(db.String(128), nullable=False, comment='是否激活')
    confirmed = db.Column(db.Boolean, nullable=False, default=False, comment='是否激活')
    confirm_time = db.Column(db.DateTime, comment='验证/激活时间')
    create_time = db.Column(db.DateTime, default=dt.datetime.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, onupdate=dt.datetime.now(), comment='更新时间')

    def create(self, commit=True):
        self.set_password(self.password)
        super(User, self).create()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """验证密码与保存的hash值是否匹配"""
        return check_password_hash(self.password, password)

    def generate_confirm_jwt(self):
        """生成确认账户的Jwt"""
        now = dt.datetime.utcnow()

        payload = dict(
            user_id=self.id,
            exp=now + dt.timedelta(seconds=60 * 60),
            iat=now,
            aud='quiz'
        )

        token = jwt.encode(payload,
                           current_app.config['SECRET_KEY'],
                           'HS256').decode('utf-8')
        return token

    def verify_confirm_jwt(self, token):
        """验证确认账户的JWT"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
                audience='quiz'
            )
        except jwt.PyJWTError:
            return False

        if payload.get('user_id') != self.id:
            return False
        self.confirmed = True
        self.confirm_time = dt.datetime.now()
        self.update()
        return True

    def get_jwt(self):
        """用户登录后, 发放有效的JWT作为JWT过期时间内的登录验证"""
        now = dt.datetime.utcnow()
        payload = dict(
            user_id=self.id,
            confirmed=self.confirmed,
            username=self.username,
            exp=now + dt.timedelta(seconds=3 * 60 * 60),
            iat=now,
            aud='quiz'
        )

        token = jwt.encode(payload,
                           current_app.config['SECRET_KEY'],
                           'HS256').decode('utf-8')
        return token

    @staticmethod
    def verify_jwt(token):
        """验证token的有效性"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
                audience='quiz'
            )
        except jwt.PyJWTError:
            return None
        return User.query.get(payload.get('user_id'))
