# -*- coding:utf-8 -*-
"""
production配置
"""
import os

# ================ sqlalchemy ================
SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')
