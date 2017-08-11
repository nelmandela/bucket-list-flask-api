
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
        print(rv.data.decode())
        self.assertEqual(json.loads(rv.data.decode()), {
            "response": [
                {
                    "bucket_id": 1,
                    "due_date": "pending",
                    "item_name": "Swim",
                    "item_status": "test item"
                }
            ]
        })

    def test_get_with_query_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get('/bucketlist/1/items/?q=Swim',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
            "response": [
                {
                    "bucket_id": 1,
                    "due_date": "pending",
                    "item_name": "Swim",
                    "item_status": "test item"
                }
            ]
        })

    def test_get_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get('/bucketlist/1/items/', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
            "response": [
                {
                    "bucket_id": 1,
                    "due_date": "pending",
                    "item_name": "Swim",
                    "item_status": "test item"
                }
            ]
        })

    def test_get_with_query_and_limit_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get(
            '/bucketlist/1/items/?q=Swim&&limit=2', headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
            "response": [
                {
                    "bucket_id": 1,
                    "due_date": "pending",
                    "item_name": "Swim",
                    "item_status": "test item"
                }
            ]
        })

    def test_get_with_limit_bucketlistItem(self):
        self.client.post(
            '/bucketlists/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.get('/bucketlist/1/items/?limit=2',
                             headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()), {
            "response": [
                {
                    "bucket_id": 1,
                    "due_date": "pending",
                    "item_name": "Swim",
                    "item_status": "test item"
                }
            ]
        })

    def test_delete_bucketlistItem(self):
        self.client.post(
            '/bucketlist/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        rv = self.client.delete('/bucketlist/1/item/1/',
                                headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         {'response': 'Bucketlist item successfully deleted.', 'status_code': 200})

    def test_update_bucketlistItem(self):
        self.client.post(
            '/bucketlist/', data=json.dumps(self.bucket), headers=self.set_header())
        self.client.post('/bucketlist/1/items/',
                         data=json.dumps(self.item), headers=self.set_header())
        self.update_item = dict(item_name="Drink salt-water",
                                item_status="test item", due_date="pending",  bucket_id=1)
        rv = self.client.put('/bucketlist/1/item/1/',
                             data=json.dumps(self.update_item), headers=self.set_header())
        self.assertEqual(json.loads(rv.data.decode()),
                         {'response': 'Item successfully updated ', 'status_code': 200})
