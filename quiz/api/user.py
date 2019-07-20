from flask import Blueprint, request

from quiz.schema.user import RegisterSchema
from quiz.resource.user import user_resource

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    :return:
    """
    reg = request.json

    reg_schema = RegisterSchema(reg)
    reg_schema.validate()
    user = user_resource.user_register(username=reg['username'],
                                       email=reg['email'],
                                       password=reg['password'])
    return dict(user)
