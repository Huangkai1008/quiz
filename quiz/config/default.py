# -*- coding:utf-8 -*-
"""
基础配置
"""
import os

# ================ flask ================
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

# ================ sqlalchemy ================
SQLALCHEMY_POOL_SIZE = os.environ.get('SQLALCHEMY_POOL_SIZE')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
SQLALCHEMY_RECORD_QUERIES = os.environ.get('SQLALCHEMY_RECORD_QUERIES')
