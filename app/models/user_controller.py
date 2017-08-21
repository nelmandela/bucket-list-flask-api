from flask import Flask, make_response, jsonify
from werkzeug.security import check_password_hash

from app.models.models import User
from app.models.models import db
import re


class UserStore(object):

    def __init__(self):
        pass

    def create_user(self, **kwargs):
        ''' creates a new user '''
        response = ""
        # validate fields
        print('' in kwargs.values())
        try:
            if '' in kwargs.values():
                return make_response(jsonify(
                    {"message": "All fields are required"}), 400)
            else:
                # check if email or username already exists
                match =\
                    re.match(
                        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                        kwargs['email'])
                if match is None:
                    return make_response(jsonify(
                        {"message": "invalid email address"}), 400)
                else:
                    user = User(kwargs['name'], kwargs['username'], kwargs['email'],
                                kwargs['password_hash'])
                    db.session.add(user)
                    db.session.commit()
                    return make_response(jsonify(
                        {"message": "User successfully created."}), 201)

        except Exception as e:
            print(str(e))
            if (str(e).find('Key (email)')) > 0 or str(e).find('UNIQUE constraint failed: user.email') > 0:
                return make_response(jsonify(
                    {"message": "email already exists."}), 201)
            elif (str(e).find('Key (username)')) > 0 or str(e).find('UNIQUE constraint failed: user.username') > 0:
                return make_response(jsonify(
                    {"message": "username already exists."}), 201)


    def login(self, username, password):
        ''' authenticates the user '''
        user = User.query.filter_by(username=username).first()
        if user:
            return check_password_hash(user.password, password)
        else:
            return False

    def authenticate(self, username):
        ''' authenticates the user '''
        user = User.query.filter_by(username=username).first()
        return user

