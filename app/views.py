from flask import render_template, request, Flask, jsonify, make_response, Blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt import JWT, jwt_required
import datetime
from functools import wraps
from flask_restful_swagger import swagger
from flask_restful import reqparse, abort, Api, Resource

from app import app
from app.models.user_controller import UserStore
from app.models.bucket_controller import BucketStore
from app.models.items_controller import ItemStore


user = UserStore()
bucket = BucketStore()
item = ItemStore()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'

api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1')

USER_DATA = {
    "masnun": "abc123"
}


class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=123)


def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}


jwt = JWT(app, verify, identity)


class Bucketlist(Resource):
    @swagger.operation(
        notes='delete a todo item by ID',
    )
    @jwt_required()
    def get(self, **kwargs):
        limit = request.args.get('limit')
        search = request.args.get('q')
        if limit:
            response = bucket.get_all_buckets_with_limit(
                limit)
            return response

        elif search:
            response = bucket.get_all_buckets_with_limit_query(search, limit)
            return response

        elif kwargs['bucket_id']:
            response = bucket.get_bucket(kwargs['bucket_id'])
            return jsonify({"response": response})

    @swagger.operation(
        notes='delete a todo item by bucket_id',
    )
    @jwt_required()
    def delete(self, **kwargs):
        response = bucket.delete(kwargs['bucket_id'])
        return response

    @swagger.operation(
        notes='delete a todo item by ID',
    )
    @jwt_required()
    def post(self, **kwargs):
        bucket_name = "mokobo"
        bucket_description = "nyarega"
        user_id = 1
        response = bucket.create_bucketlist(
            bucket_name=bucket_name, bucket_description=bucket_description, user_id=user_id)
        return jsonify({"response": response})

    @swagger.operation(
        notes='delete a todo item by ID',
    )
    @jwt_required()
    def put(self, bucket_id):
        response = bucket.update(
            bucket_id=bucket_id, bucket_name='james', bucket_description='Mathew')
        updated_response = bucket.get_bucket(bucket_id)
        response_information = ''
        if response is True:
            response_information = updated_response
        else:
            response_information = 'Bucketlist doesnt exist'
        return jsonify({"response": response_information})


class BucketlistItems(Resource):
    @swagger.operation(
        notes='delete a todo item by ID',
    )
    @jwt_required()
    def get(self, **kwargs):
        limit = request.args.get('limit')
        q = request.args.get('q')
        response = None
        if q and limit:
            response = item.get_all_buckets_with_search_limit(
                kwargs['bucket_id'], limit, q)
        elif limit:
            response = item.get_all_buckets_with_limit(
                kwargs['bucket_id'], limit)
        elif kwargs['item_id'] and kwargs['bucket_id']:
            response = item.get_item_by_id(
                kwargs['bucket_id'], kwargs['item_id'])
        return jsonify({"response": response})

    @swagger.operation(
        notes='delete a todo item by ID',
    )
    @jwt_required()
    def post(self, bucket_id):
        data = request.get_json()
        item_name = data['item_name']
        item_status = data['item_status']
        due_date = data['due_date']
        response = item.create_bucketlistitem(
            item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id)
        return jsonify({"response": response})

    @swagger.operation(
        notes='delete a todo item by ID',
    )
    @jwt_required()
    def delete(self, bucket_id, item_id):
        response = item.delete_item(bucket_id, item_id)
        return jsonify({"response": response})

    @swagger.operation(
        notes='delete a todo item by ID',
    )
    @jwt_required()
    def put(self, bucket_id, item_id):
        data = request.get_json()
        item_name = data['item_name']
        item_status = data['item_status']
        due_date = data['due_date']
        response = item.update_item(
            item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id, item_id=item_id)
        return jsonify({"response": response})


class Users(Resource):

    @jwt_required()
    def get(self, **kwargs):
        response = user.get_all()
        return jsonify({"response": response})

    def post(self, **kwargs):
        data = request.get_json()
        name = data["name"]
        username = data["username"]
        email = data["email"]
        password_hash = data["password_hash"]
        public_id = "12345"
        response = user.create_user(
            name=name, username=username, email=email, password_hash=password_hash, public_id=public_id)
        return jsonify({"response": response})


##
# Endpoints
##
api.add_resource(BucketlistItems, '/api/v01/bucketlists/<int:bucket_id>/items/<int:item_id>/',
                 '/api/v01/bucketlists/<int:bucket_id>/items/', endpoint='items')

api.add_resource(Bucketlist, '/api/v01/bucketlists/<int:bucket_id>/',
                 '/api/v01/bucketlists/', endpoint='bucketlists')

api.add_resource(Users, '/api/v01/user/<int:user_id>/',
                 '/api/v01/user/', endpoint='user')


if __name__ == '__main__':
    app.run(debug=True)
