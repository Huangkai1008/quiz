from flask import Blueprint

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/ping', methods=['GET'])
def ping():
    return dict(name='quiz', using='flask', description='Quiz is a Online q&a platform with Flask')