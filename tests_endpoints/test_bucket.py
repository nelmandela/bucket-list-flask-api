
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
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'bucket_name': 'Trip to Mars', 'bucket_id': 1, 'bucket_description': 'test', 'user_id': 1}])

    def test_create_bucketlist_with_empty_fields(self):
        self.empty_bucket = dict(bucket_name="",
                                 bucket_description="", user_id="")
        rv = self.client.post(
            '/bucketlists/', data=json.dumps(self.empty_bucket), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         { 'message': 'All fields are required'})

    def test_get_with_query_bucketlist(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.get('/bucketlists/?q=Trip to Mars&page=1',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test'}])

    def test_get_bucketlist(self):
        self.client.post('/bucketlists/', data=json.dumps(self.bucket),
                         headers=self.set_header())
        rv = self.client.get(
            '/bucketlists/', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'bucket_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'user_id': 1}])

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
        rv = self.client.get('/bucketlists/?limit=1',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), [
                         {'user_id': 1, 'bucket_name': 'Trip to Mars', 'bucket_description': 'test', 'bucket_id': 1}])

    def test_fetch_empty_buckets(self):
        rv = self.client.get('/bucketlists/?limit=1',
                             headers=self.set_header())

        self.assertEqual(json.loads(rv.data.decode()),
                         {'message': 'No Buckets'})

    def test_search_unavailable_bucket(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.get('/bucketlists/?q=hello',
                             headers=self.set_header())
        print(rv.data)
        self.assertEqual(json.loads(rv.data.decode()),
                         {'message': 'No Buckets'})

    def test_delete_bucketlist(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        rv = self.client.delete('/bucketlist/1/', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
            'message': 'Bucket successfully deleted.'})

    def test_update_bucketlist(self):
        self.client.post('/bucketlists/',
                         data=json.dumps(self.bucket), headers=self.set_header())
        self.update_bucket = dict(
            bucket_name="mathew", bucket_description="test", user_id=1)
        rv = self.client.put('/bucketlist/1/',
                             data=json.dumps(self.update_bucket), headers=self.set_header())

        self.assertEqual(json.loads(rv.data.decode()),
                         {'message': 'Bucket successfully updated.'})

    def test_share_bucketlist(self):

        # create a new bucketlist
        res = self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())

        # add bucketlist items to the created bucket
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        # user to share bucketlist with
        user = dict(name="joe", username="andela",
                    email="andela@gmail.com", password_hash="andela")
        # register first user
        print(self.client.post(
            '/auth/register/', headers={"Content-Type": "application/json"}, data=json.dumps(user)).data)

        # share bucketlist with existent user
        rv = self.client.post('/sharebucketlist/1/2',
                              data=json.dumps(self.item), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
                         'message': 'Bucketlist successfully shared'})

    def test_share_bucketlist_with_yourself(self):

        # create a new bucketlist
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())

        # add bucketlist items to the created bucket
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())

        # user to share bucketlist with
        user = dict(name="joe", username="andela",
                    email="andela@gmail.com", password_hash="andela")
        # register first user
        self.client.post(
            '/auth/register/', headers={"Content-Type": "application/json"}, data=json.dumps(user))

        # share bucketlist with yourself :(
        rv = self.client.post('/sharebucketlist/1/1',
                              data=json.dumps(self.item), headers=self.set_header())

        self.assertEqual(json.loads(rv.data.decode()), {
                         'message': 'Cannot share a bucketlist with yourself'})

    def test_share_non_existent_bucketlist(self):
        # create a new bucketlist
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())

        # add bucketlist items to the created bucket
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())

        # user to share bucketlist with
        user = dict(name="joe", username="andela",
                    email="andela@gmail.com", password_hash="andela")
        # register first user
        print(self.client.post(
            '/auth/register/', headers={"Content-Type": "application/json"}, data=json.dumps(user)).data)

        # share bucketlist with non-existent bucketlist
        rv = self.client.post('/sharebucketlist/1/4',
                              data=json.dumps(self.item), headers=self.set_header())

        self.assertEqual(json.loads(rv.data.decode()),  {
                         'message': 'user does not exist'})

    def test_share_bucketlist_non_existent_user(self):

        # create a new bucketlist
        res = self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())

        # add bucketlist items to the created bucket
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        # user to share bucketlist with
        user = dict(name="joe", username="andela",
                    email="andela@gmail.com", password_hash="andela")
        # register first user
        self.client.post(
            '/auth/register/', headers={"Content-Type": "application/json"}, data=json.dumps(user))

        # share bucketlist with existent user
        rv = self.client.post('/sharebucketlist/1/4',
                              data=json.dumps(self.item), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
                          'message': 'user does not exist'})
