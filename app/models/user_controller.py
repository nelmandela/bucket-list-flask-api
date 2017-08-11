
from werkzeug.security import  check_password_hash
from app.models.models import User
from app.models.models import db
import re


class UserStore(object):

    def __init__(self):
        pass

    def create_user(self, **kwargs):
        ''' creates a new user '''
        dictionary = {}
        # validate fields
        if kwargs['email'].strip() == '':
            dictionary['status_code'] = 400
            dictionary['response'] = 'Email is required'

        elif kwargs['username'].strip() == '':
            dictionary['status_code'] = 400
            dictionary['response'] = 'Username is required'
        elif kwargs['password_hash'].strip() == '':
            dictionary['status_code'] = 400
            dictionary['response'] = 'Password is required'
        else:
            # check if email or username already exists
            match =\
                re.match(
                    '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    kwargs['email'])
            if match is None:
                dictionary['status_code'] = 400
                dictionary['response'] = 'invalid email address'
            else:
                user = User(kwargs['name'], kwargs['username'], kwargs['email'],
                            kwargs['password_hash'])
                db.session.add(user)
                db.session.commit()
                dictionary['status_code'] = 201
                dictionary['response'] = True

        return dictionary

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



    def get_all(self):
        ''' gets all users '''
        response = User.query.all()
        user_list = []
        for user in response:
            user_container = {}
            user_container['name'] = user.name
            user_container['email'] = user.email
            user_container['id'] = user.id
            user_list.append(user_container)
        return user_list
