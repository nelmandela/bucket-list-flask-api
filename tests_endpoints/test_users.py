from flask_sqlalchemy import SQLAlchemy
import unittest
import json


from app import app
from app.models.models import db
from tests_endpoints.base_testcase import BaseTest


class TestCaseBucket(BaseTest):
    def setUp(self):
        super(TestCaseBucket, self).setUp()
        self.user = dict(name="james", username= "luke", email= "j@gmail.com", password_hash= "jacob")

    def tearDown(self):
        super(TestCaseBucket, self).tearDown()

    def test_add_user(self):
        rv = self.client.post('/api/v01/user/', data=json.dumps(self.user))
        self.assertEqual(json.loads(rv.data.decode()), {'response':True})

    def test_login_user(self):
        pass
