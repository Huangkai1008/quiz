# -*- coding:utf-8 -*-
import os
import importlib
from quiz.config import default


def config_from_object(app):
    """默认加载开发环境配置"""
    app.config.from_object(default)
    flask_env = os.environ.get('FLASK_ENV', 'development')
    config = importlib.import_module('quiz.config.%s' % flask_env)
    app.config.from_object(config)
