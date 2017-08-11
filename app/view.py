from flask import jsonify, request, json
from flask_restplus import *
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from flask_jwt import JWT, jwt_required, JWTError, current_identity

from app import app
from app.models.bucket_controller import BucketStore
from app.models.items_controller import ItemStore
from app.models.user_controller import UserStore


user = UserStore()
bucket = BucketStore()
item = ItemStore()

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(app, version='1.0', title='Bucketlist Api',
          description='Bucketlist Api',
          authorizations=authorizations,
          security='apikey'
          )

buckets = api.model('Bucketlist', {
    'bucket_name': fields.String,
    'bucket_description': fields.String,
})

login_test = api.model('UserLogin', {
    'username': fields.String,
    'password': fields.String,
})

registration = api.model('UserRegistration', {
    "username": fields.String,
    "password_hash": fields.String,
    "email": fields.String,
    "name": fields.String,
})


items = api.model('BucketlistItems', {
    'item_name': fields.String,
    'item_status': fields.String,
    'bucket_id': fields.String,
    'due_date': fields.String,
})


def verify(username, password):
    if not (username and password):
        return "invalid token"
    u = user.authenticate(username)
    if u:
        if check_password_hash(u.password, password):
            return u
    else:
        return False


def identity(payload):
    user_id = payload['identity']
    return user_id


jwt = JWT(app, verify, identity)
parser = api.parser()
parser.add_argument('task', type=str, required=True,
                    help='The task details', location='form')


@api.route('/bucketlist/<bucket_id>/', endpoint='bucketlist', methods=['GET', 'PUT', 'DELETE'])
@api.route('/bucketlists/', endpoint='bucketlists', methods=['GET', 'POST'])
class Bucketlist(Resource):

    @jwt_required()
    def get(self, **kwargs):
        limit = request.args.get('limit')
        search = request.args.get('q')
        if limit:
            response = bucket.get_all_buckets_with_limit(
                limit, int(current_identity))
            return response

        elif search:
            response = bucket.get_all_buckets_with_limit_query(
                search, limit, int(current_identity))
            return response

        elif kwargs.get("bucket_id") is not None:
            response = bucket.get_bucket(
                kwargs['bucket_id'], int(current_identity))

        else:
            response = bucket.get_bucket_list_by_id(int(current_identity))
        return jsonify({"response": response})

    @jwt_required()
    def delete(self, **kwargs):
        response = bucket.delete(kwargs['bucket_id'])
        return response

    @api.expect(buckets)
    @api.doc(parser=parser)
    @jwt_required()
    def put(self, bucket_id):
        data = request.get_json()
        response = bucket.update(
            bucket_id=bucket_id, bucket_name=data["bucket_name"], bucket_description=data["bucket_description"])
        return response

    @api.expect(buckets)
    @api.doc(parser=parser)
    @jwt_required()
    def post(self, **kwargs):
        data = request.get_json()
        bucket_name = data["bucket_name"]
        bucket_description = data["bucket_description"]
        response = bucket.create_bucketlist(
            bucket_name=bucket_name, bucket_description=bucket_description, user_id=int(current_identity))
        return jsonify({"response": response})


@api.route('/bucketlist/<bucket_id>/item/<item_id>/', endpoint='item', methods=['GET', 'PUT', 'DELETE'])
@api.route('/bucketlist/<bucket_id>/items/', endpoint='items', methods=['GET', 'POST'])
class BucketlistItems(Resource):

    @jwt_required()
    def get(self, **kwargs):
        try:
            limit = request.args.get('limit')
            q = request.args.get('q')
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
        except JWTError:
            return jsonify({"response": "Authorization required"})

    @jwt_required()
    def delete(self, bucket_id, item_id):
        response = item.delete_item(bucket_id, item_id)
        return response

    @jwt_required()
    @api.expect(items)
    @api.doc(parser=parser)
    def put(self, bucket_id, item_id):
        data = request.get_json()
        item_name = data['item_name']
        item_status = data['item_status']
        due_date = data['due_date']
        response = item.update_item(
            item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id, item_id=item_id)
        return response

    @api.expect(items)
    @api.doc(parser=parser)
    @jwt_required()
    def post(self, bucket_id):
        data = request.get_json()
        item_name = data['item_name']
        item_status = data['item_status']
        due_date = data['due_date']
        response = item.create_bucketlistitem(
            item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id)
        return response


@api.route('/auth/register/', endpoint='auth', methods=['POST', 'GET'])
class Users(Resource):

    @api.expect(registration)
    def post(self, **kwargs):
        data = request.get_json()
        name = data["name"]
        username = data["username"]
        email = data["email"]
        password_hash = generate_password_hash(data["password_hash"])
        public_id = uuid.uuid4()
        response = user.create_user(
            name=name, username=username, email=email, password_hash=password_hash, public_id=public_id)
        return jsonify({"response": response})


@api.route('/auth/login')
class Generate(Resource):
    @api.expect(login_test)
    def post(self):
        pass
