from flask import jsonify, request, json, make_response
from flask_restplus import Api, Resource, fields
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from flask_jwt import JWT, jwt_required, current_identity

from app import app
from app.models.bucket_controller import BucketStore
from app.models.items_controller import ItemStore
from app.models.user_controller import UserStore


user = UserStore()
bucket = BucketStore()
item = ItemStore()

# setting up authorization headers
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# initializing the api variable
api = Api(app, version='1.0', title='Bucketlist Api',
          description='Bucketlist Api',
          authorizations=authorizations,
          security='apikey'
          )


# create form-fields for swagger api, it makes work easier when testing the api
# --------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------


def verify(username, password):
    ''' Verify username and password '''
    if not (username and password):
        return "invalid token"
    u = user.authenticate(username)
    if u:
        if check_password_hash(u.password, password):
            return u
    else:
        return False


def identity(payload):
    ''' Getting user_id from payload to identify the current user '''
    user_id = payload['identity']
    return user_id


# initializing jwt variable
jwt = JWT(app, verify, identity)


parser = api.parser()
parser.add_argument('task', type=str, required=True,
                    help='The task details', location='form')


@api.errorhandler
def handle_custom_exception(error):
    return {'message': str(error)}, 401


@api.route('/bucketlist/<bucket_id>/', endpoint='bucketlist', methods=['GET', 'PUT', 'DELETE'])
@api.route('/bucketlists/', endpoint='bucketlists', methods=['POST', 'GET'])
class Bucketlist(Resource):

    @jwt_required()
    def get(self, **kwargs):
        ''' gets data from `bucketlist` table  '''
        limit = request.args.get('limit')
        search = request.args.get('q')
        page = request.args.get('page')

        if kwargs.get("bucket_id") is not None:
            response = bucket.get_bucket(
                kwargs['bucket_id'], int(current_identity))

        elif limit or search or page:
            response = bucket.get_all_buckets_with_limit_query(
                search, limit, int(current_identity), page)

        else:
            response = bucket.get_bucket_list_by_id(int(current_identity))
        return response

    @jwt_required()
    def delete(self, **kwargs):
        ''' deletes data from `bucketlist` table  '''
        response = bucket.delete(kwargs['bucket_id'])
        return response

    @api.expect(buckets)
    @api.doc(parser=parser)
    @jwt_required()
    def put(self, bucket_id):
        ''' updates data from `bucketlist` table  '''
        data = request.get_json()
        response = bucket.update(
            bucket_id=bucket_id, bucket_name=data["bucket_name"], bucket_description=data["bucket_description"])
        return response

    @api.expect(buckets)
    @api.doc(parser=parser)
    @jwt_required()
    def post(self, **kwargs):
        ''' adds data to `bucketlist` table  '''
        data = request.get_json()
        bucket_name = data["bucket_name"]
        bucket_description = data["bucket_description"]
        response = bucket.create_bucketlist(
            bucket_name=bucket_name, bucket_description=bucket_description, user_id=int(current_identity))
        return response


@api.route('/bucketlist/<bucket_id>/item/<item_id>/', endpoint='item', methods=['GET', 'PUT', 'DELETE'])
@api.route('/bucketlist/<bucket_id>/items/', endpoint='items', methods=['GET', 'POST'])
class BucketlistItems(Resource):

    @jwt_required()
    def get(self, **kwargs):
        ''' gets data to `bucketlistitems` table  '''
        limit = request.args.get('limit')
        q = request.args.get('q')
        page = request.args.get('page')

        if kwargs.get('item_id') and kwargs.get('bucket_id'):
            response = item.get_item_by_id(
                kwargs['bucket_id'], kwargs['item_id'])

        elif limit or q or page:
            response = item.get_all_buckets_with_search_limit(
                kwargs['bucket_id'], limit, q, page)

        else:
            response = item.get_items(kwargs.get("bucket_id"))
        return response

    @jwt_required()
    def delete(self, bucket_id, item_id):
        ''' deletes data to `bucketlistitems` table  '''
        response = item.delete_item(bucket_id, item_id)
        return response

    @jwt_required()
    @api.expect(items)
    @api.doc(parser=parser)
    def put(self, bucket_id, item_id):
        ''' updates data to `bucketlistitems` table  '''
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
        ''' adds data to `bucketlistitems` table  '''
        data = request.get_json()
        item_name = data['item_name']
        item_status = data['item_status']
        due_date = data['due_date']
        response = item.create_bucketlistitem(
            item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id)
        return response


@api.route('/sharebucketlist/<bucket_id>/<user_id>', endpoint='share', methods=['POST', 'GET'])
class ShareBucketlist(Resource):

    @jwt_required()
    def post(self, bucket_id, user_id):
        ''' shares bucketlist another user  '''

        # get bucketlist to be shared
        bucketlist = bucket.get_bucket(bucket_id, int(current_identity))

        # get bucketlist items to be shared
        bucketItems = item.get_items(bucket_id)

        # initialize response object
        new_response = None
        # print()

        # disable user sharing bucketlist to himself
        if int(user_id) == int(current_identity):
            response = make_response(jsonify(
                {"message": "Cannot share a bucketlist with yourself"}), 400)

        elif bucketlist.status_code == 200:
            # create a new bucketlist and items to target user
            try:

                response = bucket.create_bucketlist(
                    bucket_name=json.loads(bucketlist.data.decode())[
                        0]['bucket_name'],
                    bucket_description=json.loads(bucketlist.data.decode())[
                        0]['bucket_description'],
                    user_id=user_id)
            except Exception as e:
                response = make_response(jsonify(
                    {"message": "user does not exist"}), 404)

            # get latest bucketlist added by user
            # -----------------------------------------------------------------------------------
            try:
                current_bucket_id = bucket.get_bucket_list_by_id(
                    user_id)[0].get('bucket_id')
            except:
                pass

            # ------------------------------------------------------------------------------------

            # add items to the created bucketlist
            try:
                item.create_bucketlistitem(
                    item_name=json.loads(bucketlist.data.decode())[
                        0]['item_name'],
                    item_status=json.loads(bucketlist.data.decode())[
                        0]['item_status'],
                    due_date=json.loads(bucketlist.data.decode())[
                        0]['due_date'],
                    bucket_id=current_bucket_id)
            except Exception as e:
                print("Bucketlist does not have any items.")

            # if bucket successfully shared
            if json.loads(response.data.decode())['message'] == 'Bucket successfully added to user':
                response = make_response(jsonify(
                    {"message": "Bucketlist successfully shared"}), 201)
        else:
            # if bucketlist doesnt exist
            response = make_response(jsonify(
                {"message": "bucketlist does not exist"}), 404)

        return response


@api.route('/auth/register/', endpoint='auth', methods=['POST', 'GET'])
class Users(Resource):

    @api.expect(registration)
    def post(self, **kwargs):
        ''' Registers a new user '''
        data = None
        try:
            data = request.get_json()
            data['bucket_name']
        except:
            data = json.loads(request.data.decode('UTF-8'))
        name = data["name"]
        username = data["username"]
        email = data["email"]
        password_hash = generate_password_hash(data["password_hash"])
        public_id = uuid.uuid4()
        response = user.create_user(
            name=name, username=username, email=email, password_hash=password_hash, public_id=public_id)
        return response


@api.route('/auth/login')
class Generate(Resource):
    @api.expect(login_test)
    def post(self):
        ''' A router to login in the user '''
        pass
