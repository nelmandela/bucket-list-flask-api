from datetime import timedelta


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SECRET_KEY = 'josiah'
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bucket'
    JWT_AUTH_URL_RULE = '/auth/login'
    JWT_EXPIRATION_DELTA = timedelta(seconds=1200)
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(Config):
    SECRET_KEY = 'josiah'
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_buckects.db'
