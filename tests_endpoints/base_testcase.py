import unittest
import json

from app.view import *
from app.models.models import db
from app.models.user_controller import UserStore


class BaseTest(unittest.TestCase):
    def setUp(self):
        # setup test environment configuration
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bucket_test'
        self.client = app.test_client()
        self.u = UserStore()
        self.item = dict(item_name="Swim", item_status="test item",
                         due_date="pending",  bucket_id=1)
        self.user = dict(name="josiah", username="james",
                         email="j@gmail.com", password_hash="jacob")
        self.bucket = dict(bucket_name="Trip to Mars",
                           bucket_description="test", user_id=1)
        db.create_all()
        self.u.create_user(name="josiah", username="josiah",
                           email="j@gmail.com", password_hash=generate_password_hash("flask"))

    def set_header(self):
        """set header e.g Authorization and Content type"""

        response = self.client.post(
            '/auth/login',
            data=json.dumps(dict(
                username='josiah',
                password='flask'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        # A Token is needed to restrict access to certain resources
        # If not included it will result in a 401: Unauthorized Access error.

        self.token = data['access_token']

        # # Helps json to accept a JSON encoded entity from the request body.
        # # Token prefix comes before the token

        return{'Authorization': 'JWT ' + self.token,
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    def tearDown(self):
        db.session.remove
        db.drop_all()
