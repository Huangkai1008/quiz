import datetime as dt

from werkzeug.security import generate_password_hash

from quiz.model.base import Model
from quiz.extensions import db

__all__ = ['User']


class User(Model):
    """
    用户模块
    """
    _hide_columns = {'password'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=True, comment='用户名')
    email = db.Column(db.String(128), unique=True, nullable=False, comment='邮箱')
    password = db.Column('password', db.String(128), nullable=False, comment='是否激活')
    confirmed = db.Column(db.Boolean, nullable=False, default=False, comment='是否激活')
    confirm_time = db.Column(db.DateTime, comment='验证/激活时间')
    create_time = db.Column(db.DateTime, default=dt.datetime.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, onupdate=dt.datetime.now(), comment='更新时间')

    def create(self, commit=True):
        self.set_password(self.password)
        super(User, self).create()

    def set_password(self, password):
        self.password = generate_password_hash(password)
