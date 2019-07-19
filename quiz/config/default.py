# -*- coding:utf-8 -*-
"""
基础配置
"""
import os

# ================ flask ================
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

# ================ sqlalchemy ================
SQLALCHEMY_POOL_SIZE = int(os.environ.get('SQLALCHEMY_POOL_SIZE'))
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
SQLALCHEMY_RECORD_QUERIES = os.environ.get('SQLALCHEMY_RECORD_QUERIES')

# ================ flask_mail ================
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT'))
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
