from sqlalchemy import and_, exists

from quiz.extensions import db
from quiz.model.user import User, Follow


def get_user(**params):
    filters = dict()

    if params.get('user_id'):
        filters['id'] = params['user_id']
    if params.get('username'):
        filters['username'] = params['username']
    if params.get('email'):
        filters['email'] = params['email']

    query = User.query.filter_by(**filters)
    return query.first()


def get_users(**params):
    conditions = list()

    if params.get('user_ids') is not None:
        conditions.append(User.id.in_(params['user_ids']))

    query = User.query.filter(*conditions)
    return query.all()


def create_user(**attrs):
    """用户创建"""
    user = User(**attrs)
    user.create()
    return user


def create_follow(follower_id, followed_id):
    """新建关注关系"""
    follow = Follow(follower_id=follower_id, followed_id=followed_id)
    follow.create()
    return follow


def exist_follow(follower_id, followed_id):
    """判断是否有关注关系"""
    exist = db.session.query(exists().where(and_(Follow.follower_id == follower_id,
                                                 Follow.followed_id == followed_id))).scalar()
    return exist


def get_followed(follower_id):
    """获取关注的所有用户"""
    query = db.session.query(Follow.followed_id, Follow.follow_time).filter_by(follower_id=follower_id)
    return query.all()
