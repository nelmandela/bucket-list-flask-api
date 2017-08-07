import os
import sys
import config

from flask import Flask
# Add top-level directory to module search path.
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SECRET_KEY = 'asdfh87sf454yhggfd45dererfds22as112'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/bcktlst'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'


class TestingConfig(Config):
    SECRET_KEY = '8h87yhggfd45dfds22as'
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://'\
        'localhost/db_for_api_tests'
