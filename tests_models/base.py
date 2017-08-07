import unittest
from app import app
from app.views import *
from app.models.models import db
from app.models.user_controller import UserStore


class BaseTest(unittest.TestCase):
    def setUp(self):
        # setup test environment configuration
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_buckects.db'
        self.app = app.test_client()
        db.create_all()
        self.user = UserStore()
        print(self.user.create_user(name="josiah",
                                    username="james1",
                                    email="josaya@gmail.com",
                                    password_hash="jacob"))

    def tearDown(self):
        db.session.remove
        db.drop_all()
