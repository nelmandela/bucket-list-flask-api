from flask import render_template, request, Flask, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

from app import app
from app.models.user_controller import UserStore
from app.models.bucket_controller import BucketStore
from app.models.items_controller import ItemStore


user = UserStore()
bucket = BucketStore()
item  = ItemStore()


@app.route('/auth/register', methods=['POST'])
def register():
    '''
    Route enables a user to register
    '''
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'])
    name    = data['name']
    email   = data['email']
    response = user.create_user(username=username, password_hash=password, name=name, email=email, public_id=str(uuid.uuid4()))
    return jsonify({"response": response})

@app.route('/auth/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    user_response = user.login(auth.username)
    if not user_response:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    if check_password_hash(user_response.password, auth.password):
        token = jwt.encode({'public_id' : user_response.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(kwargs)
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user.get_current_user(data['public_id'])
            
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/bucketlists', methods=['POST'])
@token_required
def bucketlists(current_user):
    '''
    Route enables users to add their own bucketlist
    '''
    data = request.get_json()
    bucket_name = data['bucket_name']
    bucket_description   = data['bucket_description']
    user_id     = data['user_id']
    print(user.get_all())
    response = bucket.create_bucketlist(bucket_name=bucket_name, bucket_description=bucket_description, user_id=user_id)
    return jsonify({"response": response})

@app.route('/bucketlists/<int:bucket_id>', methods=['GET'])
@token_required
def view_bucketlists(current_user,bucket_id):
    '''
    Route enables users to view thier bucketlists by id
    '''
    response = bucket.get_bucket(bucket_id)
    print(response)
    return jsonify({"response": response})

@app.route('/bucketlists', methods=['GET'])
@token_required
def all_bucketlists(current_user):
    '''
    Route enables users to view all thier bucketlists
    '''
    response = bucket.get_all()
    print(response)
    return jsonify({"response": response})

@app.route('/bucketlists/<int:bucket_id>', methods=['PUT'])
@token_required
def update_bucketlists(current_user,bucket_id):
    '''
    Route enables users to update thier bucketlists
    '''
    data = request.get_json()
    response = bucket.update(bucket_id=bucket_id, bucket_name=data['bucket_name'], bucket_description=data['bucket_description'])
    updated_response = bucket.get_bucket(bucket_id)
    response_information = ''
    if response == True:
        response_information = updated_response
    else:
        response_information = 'Bucketlist doesnt exist'
    return jsonify({"response":response_information})

@app.route('/bucketlists/<int:bucket_id>/', methods=['DELETE'])
@token_required
def delete_bucketlists(current_user, bucket_id):
    '''
    Route enables users to delete thier bucketlists by id
    '''
    updated_response = bucket.delete(bucket_id)
    return jsonify({"response": updated_response})

@app.route('/bucketlist/<int:bucket_id>/items', methods=['POST'])
@token_required
def items_add(current_user, bucket_id):
    '''
    Route enables users to add thier bucketlists items
    '''
    data        = request.get_json()
    item_name   = data['item_name']
    item_status = data['item_status']
    due_date    = data['due_date']
    response = item.create_bucketlistitem(item_name=item_name, item_status=item_status, due_date=due_date, bucket_id=bucket_id)
    return jsonify({"response": response})



@app.route('/bucketlists/<int:bucket_id>/items', methods=['GET'])
@token_required
def get_all_items(bucket_id, current_user):
    '''
    Route enables users to view thier bucketlists items
    '''
    response = item.get_all(bucket_id)
    print(response)
    return jsonify({"response": response})


@app.route('/bucketlists/<int:bucket_id>/items/<int:item_id>', methods=['GET'])
@token_required
def get_items_by_id(current_user, bucket_id, item_id):
    '''
    Route enables users to view thier bucketlists items by id
    '''
    response = item.get_item_by_id(bucket_id, item_id)
    print(response)
    return jsonify({"response": response})

@app.route('/bucketlists/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
@token_required
def update_item(current_user, bucket_id, item_id):
    '''
    Route enables users to update thier bucketlists items
    '''
    data = request.get_json()
    item_name = data['item_name']
    item_status = data['item_status']
    due_date = data['due_date']
    response = item.update_item(bucket_id=bucket_id, item_id=item_id, item_name=item_name, item_status=item_status, due_date=due_date) 
    print(response)
    return jsonify({"response": response})

@app.route('/bucketlists/<int:bucket_id>/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(current_user, bucket_id, item_id):
    '''
    Route enables users to delete thier bucketlists items
    '''
    response = item.delete_item(bucket_id, item_id)
    print(response)
    return jsonify({"response": response})

@app.route('/allitems/', methods=['GET'])
@token_required
def all_items(current_user):
    response = item.get_items()
    print(response)
    return jsonify({"response": response})

@app.route('/users/', methods=['GET'])
@token_required
def all_users(current_user):
    response = user.get_all()
    for res in response:
        print(res.password)