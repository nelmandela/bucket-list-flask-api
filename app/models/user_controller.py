from flask import make_response, jsonify
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from app.models.models import User
from app import app
from app.models.models import db
import re


class UserStore(object):

    def __init__(self):
        pass

    def create_user(self, **kwargs):
        ''' creates a new user '''
        response = False

        # validate fields
        if kwargs['email'].strip() == '':
            response = 'Email is required'

        elif kwargs['username'].strip() == '':
            response = 'Username is required'

        elif kwargs['password_hash'].strip() == '':
            response = 'Password is required'

        else:
            # check if email or username already exists
            match =\
                re.match(
                    '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    kwargs['email'])
            if match is None:
                return 'invalid email address'
            else:
                user = User(kwargs['name'], kwargs['username'], kwargs['email'],
                            kwargs['password_hash'])
                db.session.add(user)
                db.session.commit()
                users = User.query.all()
                print(users)
                response = True

        return response

    def login(self, username):
        ''' authenticates the user '''
        user = User.query.filter_by(username=username).first()
        return user

    def get_all(self):
        ''' gets all users '''
        response = None
        response = User.query.all()
        user_list = []
        for user in response:
            user_container = {}
            user_container['name'] = user.name
            user_container['email'] = user.email
            user_container['id'] = user.id
            user_list.append(user_container)
        return user_list
