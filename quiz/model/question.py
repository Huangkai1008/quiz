import datetime as dt

from sqlalchemy import Enum
from sqlalchemy import PrimaryKeyConstraint

from quiz.extensions import db
from quiz.model.base import Model
from quiz.constants import QuestionStatus

__all__ = ['Question', 'Answer', 'AnswerVote']


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


class Answer(Model):
    """
    回答
    """
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, index=True, comment='回答用户id')
    question_id = db.Column(db.BigInteger, index=True, comment='问题id')
    content = db.Column(db.String(2048), nullable=False, comment='回答内容')
    create_time = db.Column(db.DateTime, default=dt.datetime.now(), comment='创建时间/回答时间')
    update_time = db.Column(db.DateTime, onupdate=dt.datetime.now(), comment='更新回答时间')


class AnswerVote(Model):
    """
    回答投票 包括赞同/反对
    """
    __table_args__ = (
        PrimaryKeyConstraint('answer_id', 'user_id'),
    )

    answer_id = db.Column(db.Integer, index=True, comment='回答id')
    user_id = db.Column(db.Integer, index=True, comment='赞同/反对此回答的用户id')
    agree = db.Column(db.Boolean, index=True, comment='赞同/反对')
    create_time = db.Column(db.DateTime, default=dt.datetime.now(), comment='创建时间/回答时间')
    update_time = db.Column(db.DateTime, onupdate=dt.datetime.now(), comment='更新回答时间')
