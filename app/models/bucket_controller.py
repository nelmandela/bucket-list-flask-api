from sqlalchemy_paginator import Paginator

from app.models.models import Bucketlist
from app import app
from app.models.models import db
import re
class BucketStore(object):

    def __init__(self):
        pass

    def create_bucketlist(self, **kwargs):
        '''
        method creates a new bucketlist
        '''
        message = ''
        try:
            if '' not in [kwargs['bucket_name'],
                            kwargs['bucket_description'],
                            kwargs['user_id']]:
                bucket = Bucketlist(kwargs['bucket_name'], kwargs['bucket_description'], kwargs['user_id'])
                db.session.add(bucket)
                db.session.commit()
                message = 'Bucket successfully added to user.'
        except Exception as e:
            message = 'User does not exist'
        return message
    
    def get_bucket(self, id):
        '''
        methods gets bucketlist by id
        '''
        response = None
        try:
            response = Bucketlist.query.filter_by(bucket_id=id).first()
            bucket_list = []
            bucket_container = {}
            bucket_container['bucket_name'] = response.bucket_name
            bucket_container['bucket_description'] = response.bucket_descriptions
            bucket_container['bucket_id'] = response.bucket_id
            bucket_list.append(bucket_container)
            response = bucket_list
        except Exception as e:
            response = 'Bucket not found.'
        return response
    
    def get_all(self, limit, q):
        '''
        method gets all buckectlists
        '''
        
        response = None
        if limit:
            limit = int(limit)
            if q:
                query = db.session.query(Bucketlist).filter(Bucketlist.bucket_name == q)
            else:
                query = db.session.query(Bucketlist)
            paginator = Paginator(query, limit)
            for page in paginator:
                bucket_list = []
                for bucket in page.object_list:
                    bucket_container = {}
                    bucket_container['bucket_name'] = bucket.bucket_name
                    bucket_container['bucket_description'] = bucket.bucket_descriptions
                    bucket_container['bucket_id'] = bucket.bucket_id
                    bucket_list.append(bucket_container)
                return bucket_list
        
        elif q is not None and limit is None:
            query = db.session.query(Bucketlist).filter(Bucketlist.bucket_name == q)
            paginator = Paginator(query, int(3))
            for page in paginator:
                bucket_list = []
                for bucket in page.object_list:
                    bucket_container = {}
                    bucket_container['bucket_name'] = bucket.bucket_name
                    bucket_container['bucket_description'] = bucket.bucket_descriptions
                    bucket_container['bucket_id'] = bucket.bucket_id
                    bucket_list.append(bucket_container)
                return bucket_list
        else:
            buckets = Bucketlist.query.all()
            bucket_list = []
            for bucket in buckets:
                bucket_container = {}
                bucket_container['bucket_name'] = bucket.bucket_name
                bucket_container['bucket_description'] = bucket.bucket_descriptions
                bucket_container['bucket_id'] = bucket.bucket_id
                bucket_list.append(bucket_container)
            response = bucket_list
        return response

    
    def delete(self, id):
        '''

        '''
        message = ""
        try:
            data = Bucketlist.query.filter_by(bucket_id=id).first()
            db.session.delete(data)
            db.session.commit()
            message = "Bucket successfully deleted."
        except Exception as e:
            message = "Bucket does not exist."
        return message

    def update(self, **kwargs):
        '''

        '''
        message = False
        try:
            bucket = Bucketlist.query.filter_by(bucket_id=kwargs['bucket_id']).first()
            bucket.bucket_name = kwargs['bucket_name']
            bucket.bucket_descriptions = kwargs['bucket_description']
            db.session.commit()
            message = True
        except Exception as e:
            message = False
        return message