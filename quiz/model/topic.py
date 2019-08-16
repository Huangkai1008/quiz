import datetime as dt

from sqlalchemy import PrimaryKeyConstraint

from quiz.extensions import db
from quiz.model.base import Model

__all__ = ['Article', 'Topic', 'ArticleVote']


class Topic(Model):
    """
    主题/专题
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, comment='文章作者id')
    topic_name = db.Column(db.String(54), comment='专题名')
    topic_desc = db.Column(db.String(128), comment='专题描述')
    create_time = db.Column(db.DateTime, default=dt.datetime.now(), comment='创建时间')


class Article(Model):
    """
    文章
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, comment='文章作者id')
    title = db.Column(db.String(128), comment='文章标题')
    content = db.Column(db.String(2048), comment='文章内容')
    create_time = db.Column(db.DateTime, default=dt.datetime.now(), comment='创建时间')
    topic_id = db.Column(db.Integer, index=True, comment='主题/专题id')


class ArticleVote(Model):
    """
    文章点赞, 只有点赞状态
    """
    __table_args__ = (
        PrimaryKeyConstraint('article_id', 'user_id'),
    )

    user_id = db.Column(db.Integer, index=True, comment='点赞此文章的用户id')
    article_id = db.Column(db.Integer, index=True, comment='文章id')
