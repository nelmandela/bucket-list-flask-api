import unittest
import uuid
import random
import json
import requests
import simplejson
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
        self.client = app.test_client()
        self.u = UserStore()
        self.user = dict(name="josiah", username="james",
                         email="j@gmail.com", password_hash="jacob")
        self.bucket = dict(bucket_name="Trip to Mars",
                           bucket_description="test", user_id=1)
        self.item = dict(item_name="Swim", item_status="test item",
                         due_date="pending",  bucket_id=1)
        db.create_all()

        self.headers = {"Content-Type": "application/json"}
        self.response = self.client.post(
            '/api/v01/user/', data=json.dumps(self.user))

    def tearDown(self):
        db.session.remove
        db.drop_all()
