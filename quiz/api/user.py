from flask import Blueprint, request

from quiz.schema.user import RegisterSchema

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
    return reg
