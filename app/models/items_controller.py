# from sqlalchemy_paginator import Paginator

from app.models.models import BucketlistItems
from app import app
from app.models.models import db
import re


class ItemStore(object):

    def __init__(self):
        pass

    def create_bucketlistitem(self, **kwargs):
        '''
        method creates a new bucketlist
        '''
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
        except:
            message = 'Bucket does not exist'
        return message

    def get_item_by_id(self, bucket_id, item_id):
        '''
        methods gets bucketlist by id
        '''
        response = None
        try:
            item = BucketlistItems.query.filter_by(
                bucket_id=bucket_id, item_id=item_id).first()
            print(item.bucket_id)
            item_list = []
            item_container = {}
            item_container['item_name'] = item.item_name
            item_container['item_status'] = item.item_status
            item_container['due_date'] = item.due_date
            item_container['bucket_id'] = item.bucket_id
            item_list.append(item_container)
            response = item_list
        except:
            response = 'Bucketlist item not found.'
        return response

    def get_items(self, bucket_id):
        '''
        methods gets bucketlist by id
        '''
        response = None
        paginate = BucketlistItems.query.filter(
        BucketlistItems.bucket_id == bucket_id).paginate(page=1, per_page=10)
        bucket_items = []
        for page in paginate.items:
            item_container = {}
            item_container['item_name'] = page.item_name
            item_container['item_status'] = page.item_status
            item_container['due_date'] = page.due_date
            item_container['item_id'] = page.item_id
            bucket_items.append(item_container)
        return bucket_items

# get_item_by_id

    def get_all_buckets_with_limit(self, bucket_id, limit):
        '''
        method gets all bucketlist items
        '''
        paginate = BucketlistItems.query.filter(
            BucketlistItems.bucket_id == bucket_id).paginate(page=1, per_page=int(limit))
        bucket_items = []
        for page in paginate.items:
            item_container = {}
            item_container['item_name'] = page.item_name
            item_container['item_status'] = page.item_status
            item_container['due_date'] = page.due_date
            item_container['item_id'] = page.item_id
            bucket_items.append(item_container)
        return bucket_items

    def get_all_buckets_with_search_limit(self, bucket_id, limit, q):
        '''
        method gets all bucketlist items
        '''
        paginate = BucketlistItems.query.filter(
            BucketlistItems.bucket_id == bucket_id, BucketlistItems.item_name == q).paginate(page=1, per_page=int(limit))
        bucket_items = []
        for page in paginate.items:
            item_container = {}
            if page.item_name == q:
                item_container['item_name'] = page.item_name
                item_container['item_status'] = page.item_status
                item_container['due_date'] = page.due_date
                item_container['item_id'] = page.item_id
                bucket_items.append(item_container)
        return bucket_items


    def delete_item(self, bucket_id, item_id):
        '''
        Method deletes an item from a bucketlist
        '''
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
        '''
        Method update bucketlist item
        '''
        message = False
        try:
            item = BucketlistItems.query.filter_by(
                bucket_id=kwargs['bucket_id'], item_id=kwargs['item_id']).first()
            item.item_name = kwargs['item_name']
            item.item_status = kwargs['item_status']
            item.due_date = kwargs['due_date']
            db.session.commit()
            message = "Item successfully updated "
        except Exception as e:
            message = "Bucketlist item does not exist ---"+ str(e)
        return message
