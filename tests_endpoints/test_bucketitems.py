from flask_sqlalchemy import SQLAlchemy
import unittest
import json


from app import app
from app.models.models import db
from tests_endpoints.base_testcase import BaseTest


class TestCaseBucketItems(BaseTest):
    def setUp(self):
        super(TestCaseBucketItems, self).setUp()
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        self.client.post('/api/v01/bucketlists/1/items/', data=json.dumps(self.item))


    def tearDown(self):
        super(TestCaseBucketItems, self).tearDown()
	

    def test_create_bucketlistItem(self):    
        rv = self.client.get('/api/v01/bucketlists/1/items/')
        self.assertEqual(json.loads(rv.data.decode()), {'response': [{'item_status': 'test item', 'item_id': 1, 'item_name': 'Swim', 'due_date': 'pending'}]})

    def test_get_with_query_bucketlistItem(self):
        rv = self.client.get('/api/v01/bucketlists/1/items/?q=Swim')
        self.assertEqual(json.loads(rv.data.decode()), {'response': [{'due_date': 'pending', 'item_name': 'Swim', 'item_status': 'test item', 'item_id': 1}]})

    def test_get_bucketlistItem(self):
        rv = self.client.get('/api/v01/bucketlists/1/items/')
        self.assertEqual(json.loads(rv.data.decode()), {'response': [{'due_date': 'pending', 'item_name': 'Swim', 'item_status': 'test item', 'item_id': 1}]})


    def test_get_with_query_and_limit_bucketlistItem(self):
        rv = self.client.get('api/v01/bucketlists/1/items/?q=Swim&&limit=2')
        self.assertEqual(json.loads(rv.data.decode()), {'response': [{'due_date': 'pending', 'item_name': 'Swim', 'item_status': 'test item', 'item_id': 1}]})


    def test_get_with_limit_bucketlistItem(self):
        self.client.post('/api/v01/bucketlists/1/items/', data=json.dumps(self.item))
        rv = self.client.get('api/v01/bucketlists/1/items/?limit=2')
        self.assertEqual(json.loads(rv.data.decode()), {'response': [{'due_date': 'pending', 'item_name': 'Swim', 'item_status': 'test item', 'item_id': 1}]})


    def test_delete_bucketlistItem(self):   
        rv = self.client.delete('api/v01/bucketlists/1/items/1/')
        self.assertEqual(json.loads(rv.data.decode()), {'response': 'Bucketlist item successfully deleted.'})


    def test_update_bucketlistItem(self):
        self.update_item = dict(item_name = "Drink salt-water", item_status="test item", due_date="pending",  bucket_id=1)
        rv = self.client.put('/api/v01/bucketlists/1/items/1/',data=json.dumps(self.update_item))
        self.assertEqual(json.loads(rv.data.decode()), {'response': 'Item successfully updated '})
