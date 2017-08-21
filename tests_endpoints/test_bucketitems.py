import json
from tests_endpoints.base_testcase import BaseTest


class TestCaseBucketItems(BaseTest):
    def setUp(self):
        super(TestCaseBucketItems, self).setUp()

    def tearDown(self):
        super(TestCaseBucketItems, self).tearDown()

    def test_create_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get('/bucketlist/1/items/', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         [
            {
                "bucket_id": 1,
                "due_date": "pending",
                "item_name": "Swim",
                "item_status": "test item"
            }
        ]
        )

    def test_create_bucketlistItem_with_empty_fields(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.empty_item = dict(item_name="", item_status="",
                               due_date="",  bucket_id=1)
        rv = self.client.post('/bucketlist/1/items/',
                              data=json.dumps(self.empty_item), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
                         'message': 'All fields are required'})

    def test_create_bucketlistItem_with_unavailable_bucket(self):

        rv = self.client.post('/bucketlist/4/items/',
                              data=json.dumps(self.item), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
                         'message': 'Bucket does not exist'})

    def test_get_with_query_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get('/bucketlist/1/items/?limit=1&q=S',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         [
            {
                "bucket_id": 1,
                "due_date": "pending",
                "item_name": "Swim",
                "item_status": "test item"
            }
        ]
        )

    def test_search_unavailable_bucketlistitem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get('/bucketlist/1/items/?q=1',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {'message': 'Bucketlist item not found '})

    def test_get_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get('/bucketlist/1/items/', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         [
            {
                "bucket_id": 1,
                "due_date": "pending",
                "item_name": "Swim",
                "item_status": "test item"
            }
        ]
        )

    def test_get_unavailable_bucketlistItem(self):
        rv = self.client.get('/bucketlist/1/item/1/',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
                         "response": "Bucketlist item not found."})

    def test_get_with_query_and_limit_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get(
            '/bucketlist/1/items/?q=Swim&&limit=2', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         [
            {
                "bucket_id": 1,
                "due_date": "pending",
                "item_name": "Swim",
                "item_status": "test item"
            }
        ]
        )


    def test_delete_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        response = self.client.post('/bucketlist/1/items/',
                                    data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.delete('/bucketlist/1/item/1/',
                                headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         {'message': 'Bucketlist item successfully deleted.'})

    def test_update_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        self.update_item = dict(item_name="Drink salt-water",
                                item_status="test item", due_date="pending",  bucket_id=1)
        rv = self.client.put('/bucketlist/1/item/1/',
                             data=json.dumps(self.update_item), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         {'message': 'Item successfully updated'})

    def test_update_invalid_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        self.update_item = dict(item_name="Drink salt-water",
                                item_status="test item", due_date="pending",  bucket_id=1)
        rv = self.client.put('/bucketlist/1/item/5/',
                             data=json.dumps(self.update_item), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         {'message': 'Bucketlist item does not exist'})


    def test_fetch_empty_bucketlist(self):
            self.client.post(
                '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())

            rv = self.client.get('/bucketlist/1/items/', headers=self.set_header())
            self.assertEqual(json.loads(rv.data.decode()),[])

