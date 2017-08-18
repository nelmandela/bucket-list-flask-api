from app.models.models import Bucketlist, User
from app.models.models import db


class BucketStore(object):

    def __init__(self):
        pass

    def create_bucketlist(self, **kwargs):
        ''' creates a new bucketlist '''
        buckets = {}
        try:
            if '' not in [kwargs['bucket_name'],
                          kwargs['bucket_description'],
                          kwargs['user_id']]:
                # check if user exists
                user = User.query.filter_by(
                    id=kwargs['user_id']).all()
                if len(user) == 0:
                    buckets['status_code'] = 404
                    buckets['response'] = 'user does not exist'
                else:
                    bucket = Bucketlist(
                        kwargs['bucket_name'],
                        kwargs['bucket_description'],
                        kwargs['user_id'])
                    db.session.add(bucket)
                    db.session.commit()
                    buckets['status_code'] = 201
                    buckets['response'] = 'Bucket successfully added to user.'
            else:
                buckets['status_code'] = 400
                buckets['response'] = 'All fields are required'
        except Exception as e:
            pass
        return buckets

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
        return bucket_list

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
        return bucket_list

    def get_all_buckets_with_limit(self, limit, user_id):
        ''' returns paginated bucketlists by user id  '''
        paginate = Bucketlist.query.filter_by(
            user_id=user_id).paginate(page=1, per_page=int(limit))
        return self.bucket_paginate(paginate)

    def get_all_buckets_with_limit_query(self, q, limit, user_id):
        ''' gets all buckets in a pagination object  '''
        search_limit = 3
        if limit:
            search_limit = limit

        paginate = Bucketlist.query.filter(
            Bucketlist.bucket_name.like(q+'%')).paginate(page=1,
                                                  per_page=int(search_limit))
        print(paginate)
        return self.bucket_paginate(paginate)

    def delete(self, id):
        ''' deletes  one bucketlist '''
        bucket = {}
        try:
            data = Bucketlist.query.filter_by(bucket_id=id).first()
            db.session.delete(data)
            db.session.commit()
            bucket['status_code'] = 200
            bucket['response'] = "Bucket successfully deleted."
        except:
            bucket['status_code'] = 404
            bucket['response'] = "Bucket does not exist."
        return bucket

    def get_bucket_list_by_id(self, user_id):
        ''' '''
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
            buckets['response'] = True
            buckets['status_code'] = 200
        except:
            buckets['response'] = False
            buckets['status_code'] = 404
        return buckets
