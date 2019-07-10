import os
import sentry_sdk

from sentry_sdk.integrations.flask import FlaskIntegration

from quiz.tools import QuizFlask
from quiz.config import config_from_object


def create_app():
    """Factory Pattern: Create Flask app"""
    configure_sentry()
    app = QuizFlask(__name__)

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
