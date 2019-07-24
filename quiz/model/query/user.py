from quiz.model.user import User


def get_user(**params):
    filters = dict()

    if params.get('username'):
        filters['username'] = params['username']
    if params.get('email'):
        filters['email'] = params['email']

    query = User.query.filter_by(**filters)
    return query.first()


def create_user(**attrs):
    """用户创建"""
    user = User(**attrs)
    user.create()
    return user
