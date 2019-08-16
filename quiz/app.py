import os
import logging
import traceback
import sentry_sdk

from pathlib import Path
from logging.handlers import RotatingFileHandler

from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from sentry_sdk.integrations.flask import FlaskIntegration

from quiz.tools import QuizFlask
from quiz.config import config_from_object
from quiz.api import index, user, question, topic
from quiz.extensions import cors, db, migrate, mail, redis_cli


def create_app():
    """Factory Pattern: Create Flask app"""
    configure_sentry()
    app = QuizFlask(__name__)
    configure_app(app)
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    configure_errors(app)

    return app


def configure_sentry():
    """
    配置Sentry -- 必须在Flask APP构建前初始化
    """
    sentry_sdk.init(
        dsn=os.environ.get('DSN'),
        integrations=[FlaskIntegration()]
    )


def configure_app(app):
    """配置app"""
    config_from_object(app)
    # 不检查路由中最后是否有斜杠/
    app.url_map.strict_slashes = False


def configure_blueprints(app):
    """配置蓝图"""
    app.register_blueprint(index.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(question.bp)
    app.register_blueprint(topic.bp)


def configure_extensions(app):
    """配置扩展"""
    cors.init_app(app)
    db.init_app(app)
    from quiz import model
    migrate.init_app(app, db=db, model=model)
    mail.init_app(app)
    redis_cli.init_app(app)


def configure_logging(app):
    """配置日志"""
    logger = logging.getLogger()

    stream_handler = logging.StreamHandler()

    path = Path(app.config['LOG_PATH'])
    if not path.exists():
        path.mkdir(parents=True)
    log_name = Path(path, 'quiz.log')
    file_handler = RotatingFileHandler(log_name, maxBytes=5 * 1024 * 1024, backupCount=30)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)


def configure_errors(app):
    """配置应用错误处理"""

    @app.errorhandler(404)
    def page_not_found(error):
        response = jsonify(dict(message=error.description))
        response.status_code = error.code
        return response

    @app.errorhandler(Exception)
    def exception_handle(error):
        current_app.logger.warning(traceback.format_exc())
        from quiz.exceptions import QuizException, ServerException, AuthException, NotFoundException
        if isinstance(error, (QuizException, AuthException, NotFoundException)):
            response = jsonify(dict(error))
            response.status_code = error.status_code
        elif isinstance(error, HTTPException):
            response = jsonify(dict(message=error.description))
            response.status_code = error.code
        else:
            current_app.logger.error('Server Error !')
            illegal = ServerException("服务器出现异常")
            response = jsonify(dict(illegal))
            response.status_code = illegal.status_code
        return response
