import datetime as dt

from sqlalchemy import Enum

from quiz.extensions import db
from quiz.model.base import Model
from quiz.constants import QuestionStatus

__all__ = ['Question']


class Question(Model):
    """
    问题
    """
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, index=True, comment='提问用户id')
    title = db.Column(db.String(255), unique=True, comment='标题')
    status = db.Column(Enum(QuestionStatus), default='o', comment='问题状态')
    content = db.Column(db.String(1024), nullable=True, comment='内容/详细描述')
    create_time = db.Column(db.DateTime, default=dt.datetime.now(), comment='创建时间')
    update_time = db.Column(db.DateTime, onupdate=dt.datetime.now(), comment='更新时间')
