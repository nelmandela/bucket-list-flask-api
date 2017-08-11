
import json
from tests_endpoints.base_testcase import BaseTest


class TestCaseBucket(BaseTest):
    def setUp(self):
        super(TestCaseBucket, self).setUp()

    def tearDown(self):
        super(TestCaseBucket, self).tearDown()

    def test_create_bucketlist(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.get('/bucketlists/', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {'response': [
                         {'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'user_id': 1}]})

    def test_get_with_query_bucketlist(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.get('/bucketlists/?q=Trip to Mars',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test'}])

    def test_get_bucketlist(self):
        self.client.post('/bucketlists/', data=json.dumps(self.bucket),
                         headers=self.set_header())
        rv = self.client.get(
            '/bucketlists/', headers=self.set_header())

        print(rv.data)
        self.assertEqual(json.loads(rv.data.decode()), {'response': [
                         {'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'user_id': 1}]})

    def test_get_with_query_and_limit_bucketlist(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.get(
            '/bucketlists/?q=Trip to Mars&&limit=2', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'bucket_id': 1}])

    def test_get_with_limit_bucketlist(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.get('/bucketlists/?limit=2',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'bucket_id': 1}])

    def test_delete_bucketlist(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.delete('/bucketlist/1/', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
            'response': 'Bucket successfully deleted.', 'status_code': 200})

    def test_update_bucketlist(self):
        self.client.post('/bucketlists/',
                         data=json.dumps(self.bucket), headers=self.set_header())
        self.update_bucket = dict(
            bucket_name="mathew", bucket_description="test", user_id=1)
        rv = self.client.put('/bucketlist/1/',
                             data=json.dumps(self.update_bucket), headers=self.set_header())

        self.assertEqual(json.loads(rv.data.decode()),
                         {'response': True, 'status_code': 200})
