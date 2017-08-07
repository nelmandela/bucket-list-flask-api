import uuid

from flask import Flask, json, jsonify, request, session
from flask.ext.restful import Api, Resource
from flask_restful_swagger import swagger
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from app.models.bucket_controller import BucketStore
from app.models.items_controller import ItemStore
from app.models.user_controller import UserStore
from flask_jwt import JWT, jwt_required

user = UserStore()
bucket = BucketStore()
item = ItemStore()

###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
api = swagger.docs(Api(app), apiVersion='0.1')
###################################



def verify(username, password):
    if not (username and password):
        return "invalid token"
    u = user.login(username)
    if u:
        if check_password_hash(u.password, password):
            session['user_id'] = u.id
            return u
    else:
        return False


def identity(payload):
    user_id = payload['identity']
    return user_id


jwt = JWT(app, verify, identity)


class Bucketlist(Resource):

    # @jwt_required()
    '''Describing elephants'''
    @swagger.operation(
        notes='some really good notes',
        responseClass='ModelClass.__name__',
        nickname='upload',
        parameters=[
            {
                "name": "body",
                "description": "blueprint object that needs to be added. YAML.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'ModelClass2.__name__',
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created. The URL of the created blueprint should be in the Location header"
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def get(self, **kwargs):
        limit = request.args.get('limit')
        search = request.args.get('q')
        if limit:
            response = bucket.get_all_buckets_with_limit(
                limit, 1)
            return response

        elif search:
            response = bucket.get_all_buckets_with_limit_query(
                search, limit, 1)
            return response

        elif kwargs.get("bucket_id") is not None:
            response = bucket.get_bucket(kwargs['bucket_id'], 1)

        else:
            response = bucket.get_bucket_list_by_id(1)
        return jsonify({"response": response})

    # @jwt_required()
    def delete(self, **kwargs):
        response = bucket.delete(kwargs['bucket_id'])
        return jsonify({"response": response})

    # @jwt_required()
    def post(self, **kwargs):
        data = None
        try:
            data = request.get_json()
            data['bucket_name']
        except:
            data = json.loads(request.data.decode('UTF-8'))
        bucket_name = data["bucket_name"]
        bucket_description = data["bucket_description"]
        # user_id = session['user_id']
        response = bucket.create_bucketlist(
            bucket_name=bucket_name, bucket_description=bucket_description, user_id=data["user_id"])
        return jsonify({"response": response})

    # @jwt_required()
    def put(self, bucket_id):
        data = None
        try:
            data = request.get_json()
            data['bucket_name']
        except:
            data = json.loads(request.data.decode('UTF-8'))
        response = bucket.update(
            bucket_id=bucket_id, bucket_name=data["bucket_name"], bucket_description=data["bucket_description"])
        updated_response = bucket.get_bucket(bucket_id, 1)
        response_information = ''
        if response is True:
            response_information = updated_response
        else:
            response_information = 'Bucketlist doesnt exist'
        return jsonify({"response": response_information})


class BucketlistItems(Resource):

    # @jwt_required()
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

        elif kwargs.get('item_id') and kwargs.get('bucket_id'):
            response = item.get_item_by_id(
                kwargs['bucket_id'], kwargs['item_id'])
        else:
            response = item.get_items(kwargs.get("bucket_id"))
        return jsonify({"response": response})

    # @jwt_required()
    def post(self, bucket_id):
        data = None
        try:
            data = request.get_json()
            data['bucket_name']
        except:
            data = json.loads(request.data.decode('UTF-8'))
        item_name = data['item_name']
        item_status = data['item_status']
        due_date = data['due_date']
        response = item.create_bucketlistitem(
            item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id)
        return jsonify({"response": response})

    # @jwt_required()
    def delete(self, bucket_id, item_id):
        response = item.delete_item(bucket_id, item_id)
        return jsonify({"response": response})

    # @jwt_required()
    def put(self, bucket_id, item_id):
        data = None
        try:
            data = request.get_json()
            data['bucket_name']
        except:
            data = json.loads(request.data.decode('UTF-8'))
        item_name = data['item_name']
        item_status = data['item_status']
        due_date = data['due_date']
        response = item.update_item(
            item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id, item_id=item_id)
        return jsonify({"response": response})


class Users(Resource):

    # @jwt_required()
    def get(self, **kwargs):
        response = user.get_all()
        return jsonify({"response": response})

    def post(self, **kwargs):
        data = None
        try:
            data = request.get_json()
            data['name']
        except:
            data = json.loads(request.data.decode('UTF-8'))
        name = data["name"]
        username = data["username"]
        email = data["email"]
        password_hash = data["password_hash"]
        public_id = uuid.uuid4()
        response = user.create_user(
            name=name, username=username, email=email, password_hash=generate_password_hash(password_hash), public_id=public_id)
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
