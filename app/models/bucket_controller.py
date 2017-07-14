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
    
    def get_all(self):
        '''
        method gets all buckectlists
        '''
        buckets = Bucketlist.query.all()
        bucket_list = []
        for bucket in buckets:
            bucket_container = {}
            bucket_container['bucket_name'] = bucket.bucket_name
            bucket_container['bucket_description'] = bucket.bucket_descriptions
            bucket_container['bucket_id'] = bucket.bucket_id
            bucket_list.append(bucket_container)
        return bucket_list
    
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