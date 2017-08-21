from flask import Flask, make_response, jsonify

from app.models.models import Bucketlist, User
from app.models.models import db


class BucketStore(object):

    def __init__(self):
        pass

    def create_bucketlist(self, **kwargs):
        ''' creates a new bucketlist '''
        response = {}
        try:
            if '' not in [kwargs['bucket_name'],
                          kwargs['bucket_description'],
                          kwargs['user_id']]:
                # check if user exists
                user = User.query.filter_by(
                    id=kwargs['user_id']).all()
                if len(user) == 0:
                    response = make_response(jsonify(
                        {"message": "user does not exist"}), 404)
                else:
                    bucket = Bucketlist(
                        kwargs['bucket_name'],
                        kwargs['bucket_description'],
                        kwargs['user_id'])
                    db.session.add(bucket)
                    db.session.commit()
                    response = make_response(jsonify(
                        {"message": "Bucket successfully added to user"}), 201)
            else:
                response = make_response(jsonify(
                    {"message": "All fields are required"}), 400)
        except Exception as e:
            pass
        return response

    def get_bucket(self, bucket_id, user_id):
        ''' gets bucketlist by id '''
        data = Bucketlist.query.filter_by(
            bucket_id=bucket_id, user_id=user_id).all()
        response = self.bucket_obj_unpacks(data)
        return response

    def bucket_obj_unpacks(self, data):
        ''' unpacks orm data object '''
        bucket_list = []
        for bucket in data:
            bucket_container = {}
            bucket_container['bucket_name'] = bucket.bucket_name
            bucket_container['bucket_description'] = bucket.bucket_descriptions
            bucket_container['bucket_id'] = bucket.bucket_id
            bucket_container['user_id'] = bucket.user_id
            bucket_list.append(bucket_container)
        if len(bucket_list) > 0:
            return make_response(jsonify(bucket_list), 200)
        else:
            return make_response(jsonify({"message": "No Buckets"}), 404)

    def bucket_paginate(self, paginate_obj):
        ''' unpacks pagination object '''
        bucket_list = []
        for page in paginate_obj.items:
            bucket_container = {}
            bucket_container['bucket_name'] = page.bucket_name
            bucket_container['bucket_description'] = page.bucket_descriptions
            bucket_container['bucket_id'] = page.bucket_id
            bucket_container['user_id'] = page.user_id
            bucket_list.append(bucket_container)
        if len(bucket_list) > 0:
            return make_response(jsonify(bucket_list), 200)
        else:
            return make_response(jsonify({"message": "No Buckets"}), 404)

    def get_all_buckets_with_limit_query(self, q=None, limit=1, user_id=1, page=1):
        ''' gets all buckets in a pagination object  '''

        if limit is None or '':
            limit = 1
        else:
            limit = int(limit)
        if page is None or '':
            page = 1
        else:
            page = int(page)
        print(user_id)
        try:
            if q:
                paginate = Bucketlist.query.filter(
                    Bucketlist.bucket_name.like(q + '%'), Bucketlist.user_id == user_id).paginate(page=page, per_page=limit)
            else:
                paginate = Bucketlist.query.filter(Bucketlist.user_id==user_id).paginate(page=page,
                                                                                        per_page=limit)
            return self.bucket_paginate(paginate)
        except Exception as e:
            return make_response(jsonify({"message": "Bucketlist not found"}), 404)

    def delete(self, id):
        ''' deletes  one bucketlist '''
        response = ""
        try:
            data = Bucketlist.query.filter_by(bucket_id=id).first()
            db.session.delete(data)
            db.session.commit()
            response = make_response(jsonify(
                {"message": "Bucket successfully deleted."}), 201)
        except:
            response = make_response(jsonify(
                {"message": "Bucket does not exist."}), 404)
        return response

    def get_bucket_list_by_id(self, user_id):
        ''' gets all bucketlist by User Id '''
        data = Bucketlist.query.filter_by(user_id=user_id).all()
        return self.bucket_obj_unpacks(data)

    def update(self, **kwargs):
        ''' updates bucketlist '''
        buckets = {}
        try:
            bucket = Bucketlist.query.filter_by(
                bucket_id=kwargs['bucket_id']).first()
            bucket.bucket_name = kwargs['bucket_name']
            bucket.bucket_descriptions = kwargs['bucket_description']
            db.session.commit()
            response = make_response(jsonify(
                {"message": "Bucket successfully updated."}), 201)
        except:
            response = make_response(jsonify(
                {"message": "Bucket does not exist."}), 404)
        return response
