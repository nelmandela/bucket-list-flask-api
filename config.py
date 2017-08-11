
class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SECRET_KEY = 'josiah'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bucket'
    JWT_AUTH_URL_RULE = '/auth/login'


class TestingConfig(Config):
    SECRET_KEY = 'josiah'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bucket_test'
