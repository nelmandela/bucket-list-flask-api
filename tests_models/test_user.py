#!flask/bin/python
import unittest
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user_controller import UserStore
from app.models.models import *
from tests_models.base import BaseTest
from app.models.models import db
from app import app

user = UserStore()


class UserTestCase(BaseTest):
    def setUp(self):
        super(UserTestCase, self).setUp()

    def test_create_user(self):
        response = user.create_user(email='john@example.com', username='josiah',
                                    password_hash=generate_password_hash('pass'), name='jos')
        current_user = User.query.filter_by(username='josiah').first()
        assert current_user.username == 'josiah'

    def test_invalid_email_address(self):
        response = user.create_user(email='invalidEmail', username='josiah',
                                    password_hash=generate_password_hash('pass'), name='jos')
        users = User.query.all()
        self.assertEqual('invalid email address', response)

    def test_login_user_not_availabe(self):
        user.create_user(email='john@example.com', username='josiah',
                         password_hash=generate_password_hash('pass'), name='jos')
        response = user.login(username='josiah')
        self.assertEqual(response.username, 'josiah')

    def test_current_user(self):
        user.create_user(email='john@example.com', username='josiah',
                         password_hash=generate_password_hash('pass'), name='jos')
        response = User.query.all()
        self.assertEqual(int(User.query.filter_by(
            username='josiah').first().id), 2)

    def test_empty_inputs(self):
        response = user.create_user(
            email='email@correct.email', username='', password_hash='', name='')
        users = User.query.all()
        self.assertEqual('Username is required', response)

    def test_get_all(self):
        user.create_user(email='example@correct.com', username='james',
                         password_hash=generate_password_hash('12345'), name='josiah')
        user.create_user(email='johns@example.com', username='josh',
                         password_hash=generate_password_hash('123454'), name='josiah')
        users = User.query.all()
        self.assertEqual(len(users), 3)

    def test_password_hashing(self):
        user.create_user(email='example@correct.com', username='james',
                         password_hash=generate_password_hash('12345'), name='josiah')
        users = User.query.filter_by(username='james').first()
        self.assertEqual(check_password_hash(users.password, '12345'), True)

    def tearDown(self):
        super(UserTestCase, self).tearDown()
