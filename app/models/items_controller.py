from flask import Flask, make_response, jsonify

from app.models.models import BucketlistItems, Bucketlist
from app.models.models import db


class ItemStore(object):

    def __init__(self):
        pass

    def create_bucketlistitem(self, **kwargs):
        ''' creates a new bucket item '''
        response = ""
        if '' not in [kwargs['item_name'],
                      kwargs['item_status'],
                      kwargs['due_date'],
                      kwargs['bucket_id']]:
            check_id = Bucketlist.query.filter_by(
                bucket_id=kwargs['bucket_id']).all()
            if len(check_id) > 0:
                bucketitems = BucketlistItems(
                    kwargs['item_name'], kwargs['item_status'], kwargs['due_date'], kwargs['bucket_id'])
                db.session.add(bucketitems)
                db.session.commit()
                response = make_response(jsonify(
                    {"message": "Bucketlist item successfully added to user."}), 201)
            else:
                response = make_response(jsonify(
                    {"message": "Bucket does not exist"}), 404)
        else:
            response = make_response(jsonify(
                {"message": "All fields are required"}), 400)
        return response

    def get_item_by_id(self, bucket_id, item_id):
        ''' returns bucket item by id '''
        try:
            item = BucketlistItems.query.filter_by(
                bucket_id=bucket_id, item_id=item_id).first()
            item_list = []
            item_dict = {}
            item_dict['item_name'] = item.item_name
            item_dict['item_status'] = item.item_status
            item_dict['due_date'] = item.due_date
            item_dict['bucket_id'] = item.bucket_id
            item_list.append(item_dict)
            response = item_list
        except:
            response = {'response': 'Bucketlist item not found.'}
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
        if len(item_list) > 0:
            return make_response(jsonify(item_list), 200)
        else:
            return make_response(jsonify(item_list), 404)

    def item_paginate(self, paginate_obj):
        ''' unpacks pagination object '''
        item_list = []
        for page in paginate_obj.items:
            item_container = {}
            item_container['item_name'] = page.item_name
            item_container['item_status'] = page.item_status
            item_container['due_date'] = page.due_date
            item_container['bucket_id'] = page.bucket_id
            item_list.append(item_container)
        if len(item_list) > 0:
            return make_response(jsonify(item_list), 200)
        else:
            return make_response(jsonify(item_list), 404)

    def get_all_buckets_with_search_limit(self, bucket_id, limit, q, page):
        '''  gets all bucketlist items by id and returns a pagination object'''
        if limit is None:
            limit = 1
        elif page is None:
            page = 1
        try:
            paginate = BucketlistItems.query.filter(
                BucketlistItems.bucket_id == bucket_id).paginate(page=int(page), per_page=int(limit))
            return self.item_paginate(paginate)
        except:
            return make_response(jsonify({"message": "Bucketlist item not found "}), 404)

    def delete_item(self, bucket_id, item_id):
        ''' deletes an item from a bucketlist '''
        response = ""
        try:
            items = BucketlistItems.query.filter_by(
                bucket_id=bucket_id, item_id=item_id).first()
            db.session.delete(items)
            db.session.commit()
            response = make_response(jsonify(
                {"message": "Bucketlist item successfully deleted."}), 201)
        except:
            response = make_response(jsonify(
                {"message": "Bucketlist item does not exist."}), 404)
        return response

    def update_item(self, **kwargs):
        ''' updates bucketlist item '''
        response = ""
        try:
            items = BucketlistItems.query.filter_by(
                bucket_id=kwargs['bucket_id'], item_id=kwargs['item_id']).first()
            items.item_name = kwargs['item_name']
            items.item_status = kwargs['item_status']
            items.due_date = kwargs['due_date']
            db.session.commit()
            response = make_response(jsonify(
                {"message": "Item successfully updated"}), 201)
        except:
            response = make_response(jsonify(
                {"message": "Bucketlist item does not exist"}), 404)
        return response
