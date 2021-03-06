from flask import Blueprint, request, g

from quiz.model.user import User
from quiz.model.queries import user as user_api
from quiz.schema.user import RegisterSchema, LoginSchema
from quiz.resource import user as user_resource
from quiz.resource.auth import token_auth
from quiz.exceptions import ValidateException, AuthException

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    :return:
    """
    reg_schema = RegisterSchema(request.json)
    reg_schema.validate()
    user = user_resource.user_register(
        username=reg_schema['username'],
        email=reg_schema['email'],
        password=reg_schema['password'],
    )
    return dict(user)


@bp.route('/confirm/<string:token>', methods=['GET'])
def confirm(token):
    """用户收到验证邮件后，验证其账户"""
    g.current_user = User.verify_jwt(token) if token else None
    if g.current_user:
        if g.current_user.confirmed:
            raise ValidateException('账户已被验证, 无需重复验证')

        if g.current_user.verify_confirm_jwt(token):
            token = g.current_user.get_jwt()
            return dict(
                token=token, message='You have confirmed your account, thanks! '
            )
        else:
            raise ValidateException('The confirmation link is invalid or has expired')

    else:
        raise ValidateException('The token is invalid')


@bp.route('/resend-confirm', methods=['POST'])
def resend_confirm():
    """重新发送验证邮件"""
    reg = request.json
    if 'email' not in reg:
        raise ValidateException('请输入要重新发送注册邮件的邮箱')
    user_resource.resend_confirm_email(email=reg['email'])
    return dict()


@bp.route('/tokens', methods=['POST'])
def get_token():
    """获取token, 前端获取到刷新后的token放到请求头中就可以不需要再登录"""
    login_schema = LoginSchema(request.json)
    login_schema.validate()

    user = user_api.get_user(username=login_schema['username'])
    if not user.confirmed:
        raise ValidateException('账户尚未验证, 请检查邮箱验证账户')

    if user.check_password(login_schema['password']):
        token = user.get_jwt()
        return dict(token=token)
    else:
        raise AuthException('用户名和密码不匹配')


@bp.route('/followed', methods=['GET'])
@token_auth.login_required
def followed_get():
    """获取该用户下所有的关注用户"""
    users = user_resource.get_followed()
    return dict(users=users)


@bp.route('/follow/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def follow(user_id):
    """开始关注新用户"""
    user_resource.follow_user(user_id)
    return dict()
