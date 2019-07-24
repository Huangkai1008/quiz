from flask import Blueprint, request

bp = Blueprint('question', __name__, url_prefix='/questions')


@bp.route('/', methods=['GET'])
def questions():
    """
    问题列表
    :return:
    """
    pass
