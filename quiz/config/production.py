# -*- coding:utf-8 -*-
"""
production配置
"""
import os

# ================ sqlalchemy ================
SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')

# ================ additional ================
CONFIRM_EMAIL_URL = os.environ.get('PRODUCTION_CONFIRM_EMAIL_URL')
