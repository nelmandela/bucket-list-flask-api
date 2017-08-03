from app.models.models import Bucketlist
from app.models.models import db

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
                bucket = Bucketlist(
                    kwargs['bucket_name'], kwargs['bucket_description'], kwargs['user_id'])
                db.session.add(bucket)
                db.session.commit()
                message = 'Bucket successfully added to user.'
            else:
                message = 'All fields are required'
        except Exception as e:
            message = 'Bucket not created'
        return message

    def get_bucket(self, bucket_id, user_id):
        '''
        methods gets bucketlist by id
        '''
        response = None
        try:
            response = Bucketlist.query.filter_by(user_id=user_id).filter_by(bucket_id=bucket_id).first()
            bucket_list = []
            bucket_container = {}
            bucket_container['bucket_name'] = response.bucket_name
            bucket_container['bucket_description'] = response.bucket_descriptions
            bucket_container['bucket_id'] = response.bucket_id
            bucket_container['user_id'] = response.user_id
            bucket_list.append(bucket_container)
            response = bucket_list
        except Exception as e:
            response = 'Bucket not found'
        return response

    def get_all_buckets_with_limit(self, limit, user_id):
        '''
        method gets all buckectlists
        '''
        paginate = Bucketlist.query.filter_by(user_id=user_id).paginate(page=1, per_page=int(limit))
        bucket_list = []
        for page in paginate.items:
            bucket_container = {}
            bucket_container['bucket_name'] = page.bucket_name
            bucket_container['bucket_description'] = page.bucket_descriptions
            bucket_container['bucket_id'] = page.bucket_id
            bucket_container['user_id'] = page.user_id
            bucket_list.append(bucket_container)
        return bucket_list

    def get_all_buckets_with_limit_query(self, q, limit, user_id):
        ''' Method '''
        search_limit = 3
        if limit:
            search_limit = limit

        paginate = Bucketlist.query.filter(
            Bucketlist.bucket_name == q).paginate(page=1, per_page=int(search_limit))
        bucket_list = []
        for page in paginate.items:
            bucket_container = {}
            if page.user_id == user_id:
                bucket_container['bucket_name'] = page.bucket_name
                bucket_container['bucket_description'] = page.bucket_descriptions
                bucket_container['bucket_id'] = page.bucket_id
                bucket_container['user_id'] = page.user_id
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
        except:
            message = "Bucket does not exist."
        return message

    def get_bucket_list_by_id(self, user_id):
        ''' '''
        data = Bucketlist.query.filter_by(user_id=user_id).all()
        bucket_list = []
        for bucket in data:
            bucket_container = {}
            bucket_container['bucket_name'] = bucket.bucket_name
            bucket_container['bucket_description'] = bucket.bucket_descriptions
            bucket_container['bucket_id'] = bucket.bucket_id
            bucket_container['user_id'] = bucket.user_id
            bucket_list.append(bucket_container)
        return bucket_list


    def update(self, **kwargs):
        '''

        '''
        message = False
        try:
            bucket = Bucketlist.query.filter_by(
                bucket_id=kwargs['bucket_id']).first()
            bucket.bucket_name = kwargs['bucket_name']
            bucket.bucket_descriptions = kwargs['bucket_description']
            db.session.commit()
            message = True
        except:
            message = False
        return message
