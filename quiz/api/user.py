from flask import Blueprint, request, g

from quiz.model.user import User
from quiz.model.query import user as user_api
from quiz.schema.user import RegisterSchema, LoginSchema
from quiz.resource import user as user_resource
from quiz.exceptions import ValidateException, AuthException

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


@bp.route('/confirm/<string:token>', methods=['GET'])
def confirm(token):
    """用户收到验证邮件后，验证其账户"""
    g.current_user = User.verify_jwt(token) if token else None
    if g.current_user:
        if g.current_user.confirmed:
            raise ValidateException('账户已被验证, 无需重复验证')

        if g.current_user.verify_confirm_jwt(token):
            token = g.current_user.get_jwt()
            return dict(token=token, message='You have confirmed your account, thanks! ')
        else:
            raise ValidateException('The confirmation link is invalid or has expired')

    else:
        raise ValidateException('The token is invalid')


@bp.route('/resend-confirm', methods=['GET'])
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
    login = request.json
    login_schema = LoginSchema(login)
    login_schema.validate()

    user = user_api.user_first(username=login['username'])
    if not user.confirmed:
        raise ValidateException('账户尚未验证, 请检查邮箱验证账户')

    if user.check_password(login['password']):
        token = user.get_jwt()
        return dict(token=token)
    else:
        raise AuthException('用户名和密码不匹配')
