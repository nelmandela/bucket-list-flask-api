# from sqlalchemy_paginator import Paginator
from sqlalchemy.exc import IntegrityError

from app.models.models import BucketlistItems
from app import app
from app.models.models import db
import re


class ItemStore(object):

    def __init__(self):
        pass

    def create_bucketlistitem(self, **kwargs):
        ''' creates a new bucket item '''
        message = ''
        try:
            if '' not in [kwargs['item_name'],
                          kwargs['item_status'],
                          kwargs['due_date'],
                          kwargs['bucket_id']]:
                bucket = BucketlistItems(
                    kwargs['item_name'], kwargs['item_status'], kwargs['due_date'], kwargs['bucket_id'])
                db.session.add(bucket)
                db.session.commit()
                message = 'Bucketlist item successfully added to user.'
            else:
                message = 'All fields are required'
        except IntegrityError as e:
            message = 'Item name already exists.'
        except Exception as e:
            message = 'Bucket does not exist'
        return message

    def get_item_by_id(self, bucket_id, item_id):
        ''' returns bucket item by id '''
        response = None
        try:
            item = BucketlistItems.query.filter_by(
                bucket_id=bucket_id, item_id=item_id).first()
            response = self.item_obj_unpacks(item)
        except:
            response = 'Bucketlist item not found.'
        return response

    def get_items(self, bucket_id):
        ''' methods gets bucketlist by id '''
        paginate = BucketlistItems.query.filter(
            BucketlistItems.bucket_id == bucket_id).paginate(page=1, per_page=10)
        return self.item_paginate(paginate)

    def item_obj_unpacks(self, data):
        ''' unpacks orm data object '''
        item_list = []
        for item in data:
            item_container = {}
            item_container['item_status'] = item.item_status
            item_container['item_status'] = item.item_status
            item_container['due_date'] = item.due_date
            item_container['bucket_id'] = item.bucket_id
            item_list.append(item_container)
        return item_list

    def item_paginate(self, paginate_obj):
        ''' unpacks pagination object '''
        item_list = []
        for page in paginate_obj.items:
            item_container = {}
            item_container['item_status'] = page.item_status
            item_container['item_status'] = page.item_status
            item_container['due_date'] = page.due_date
            item_container['bucket_id'] = page.bucket_id
            item_list.append(item_container)
        return item_list

# get_item_by_id

    def get_all_buckets_with_limit(self, bucket_id, limit):
        ''' gets all bucketlist items by bucket id'''
        paginate = BucketlistItems.query.filter(
            BucketlistItems.bucket_id == bucket_id).paginate(page=1, per_page=int(limit))
        return self.item_paginate(paginate)

    def get_all_buckets_with_search_limit(self, bucket_id, limit, q):
        '''  gets all bucketlist items by id and returns a pagination object'''
        paginate = BucketlistItems.query.filter(
            BucketlistItems.bucket_id == bucket_id, BucketlistItems.item_name == q).paginate(page=1, per_page=int(limit))
        return self.item_paginate(paginate)

    def delete_item(self, bucket_id, item_id):
        ''' deletes an item from a bucketlist '''
        message = ""
        try:
            item = BucketlistItems.query.filter_by(
                bucket_id=bucket_id, item_id=item_id).first()
            db.session.delete(item)
            db.session.commit()
            message = "Bucketlist item successfully deleted."
        except:
            message = "Bucketlist item does not exist."
        return message

    def update_item(self, **kwargs):
        ''' updates bucketlist item '''
        message = False
        try:
            item = BucketlistItems.query.filter_by(
                bucket_id=kwargs['bucket_id'], item_id=kwargs['item_id']).first()
            item.item_name = kwargs['item_name']
            item.item_status = kwargs['item_status']
            item.due_date = kwargs['due_date']
            db.session.commit()
            message = "Item successfully updated "
        except:
            message = "Bucketlist item does not exist"
        return message
