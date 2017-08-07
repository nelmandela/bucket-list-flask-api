from flask_sqlalchemy import SQLAlchemy
import unittest
import json


from app import app
from app.models.models import db
from tests_endpoints.base_testcase import BaseTest


class TestCaseBucket(BaseTest):
    def setUp(self):
        super(TestCaseBucket, self).setUp()

    def tearDown(self):
        super(TestCaseBucket, self).tearDown()

    def test_create_bucketlist(self):
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        rv = self.client.get('/api/v01/bucketlists/')
        self.assertEqual(json.loads(rv.data.decode()), {'response': [
                         {'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'user_id': 1}]})

    def test_get_with_query_bucketlist(self):
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        rv = self.client.get('/api/v01/bucketlists/?q=Trip to Mars')
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test'}])

    def test_get_bucketlist(self):
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        rv = self.client.get('/api/v01/bucketlists/')
        self.assertEqual(json.loads(rv.data.decode()), {'response': [
                         {'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'user_id': 1}]})

    def test_get_with_query_and_limit_bucketlist(self):
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        rv = self.client.get('/api/v01/bucketlists/?q=Trip to Mars&&limit=2')
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'bucket_id': 1}])

    def test_get_with_limit_bucketlist(self):
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        rv = self.client.get('/api/v01/bucketlists/?limit=2')
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'bucket_id': 1}])

    def test_delete_bucketlist(self):
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        rv = self.client.delete('/api/v01/bucketlists/1/')
        self.assertEqual(json.loads(rv.data.decode()), {
                         'response': 'Bucket successfully deleted.'})

    def test_update_bucketlist(self):
        self.client.post('/api/v01/bucketlists/', data=json.dumps(self.bucket))
        self.update_bucket = dict(
            bucket_name="mathew", bucket_description="test", user_id=1)
        rv = self.client.put('/api/v01/bucketlists/1/',
                             data=json.dumps(self.update_bucket))
        self.assertEqual(json.loads(rv.data.decode()), {'response': [
                         {'user_id': 1, 'bucket_id': 1, 'bucket_description': 'test', 'bucket_name': 'mathew'}]})
