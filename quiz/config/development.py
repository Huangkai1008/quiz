# -*- coding:utf-8 -*-
"""
development配置
"""
import os
from pathlib import Path

# ================ sqlalchemy ================
SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URL')

# ================ redis ================
REDIS_URL = os.environ.get('DEVELOPMENT_REDIS_URL')

# ================ additional ================
ROOT_PATH = Path.cwd()  # 根目录 /quiz
LOG_PATH = Path(ROOT_PATH, 'logs')  # 日志目录
CONFIRM_EMAIL_URL = os.environ.get('DEVELOPMENT_CONFIRM_EMAIL_URL')
