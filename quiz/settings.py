import os


class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', default='development')
    DEBUG = FLASK_ENV == 'development'
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.getenv('REDIS_URL')

    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    broker_url = os.getenv('broker_url')
    result_backend = os.getenv('result_backend')

    DSN = os.getenv('DSN')

    LOG_PATH = os.getenv('LOG_PATH')

    CONFIRM_EMAIL_URL = os.getenv('CONFIRM_EMAIL_URL')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)
