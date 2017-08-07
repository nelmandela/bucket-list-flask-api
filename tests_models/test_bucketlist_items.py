#!flask/bin/python
from app.models.items_controller import ItemStore
from app.models.bucket_controller import BucketStore

from app.models.models import db
from app import app
from tests_models.base import BaseTest
item = ItemStore()
bucket = BucketStore()


class BucketItemsTestCase(BaseTest):
    def setUp(self):
        super(BucketItemsTestCase, self).setUp()

    def test_create_bucket_item(self):
        bucket.create_bucketlist(bucket_name='Journey to the moon',
                                 bucket_description='use a rocket to fly', user_id=1)
        response = item.create_bucketlistitem(item_name='Eat chinese food',
                                              item_status='pending',
                                              due_date='12-03-2017',
                                              bucket_id='1')
        self.assertEqual(
            response, 'Bucketlist item successfully added to user.')

    def test_pagination_in_bucketlists_items(self):
        bucket.create_bucketlist(bucket_name='Journey to the moon',
                                 bucket_description='use a rocket to fly', user_id=1)
        item.create_bucketlistitem(item_name='Journey to the usa',
                                   item_status='use a aeroplane to travel',
                                   due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the japan',
                                   item_status='pending',
                                   due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='pending',
                                   due_date='12-08-2019', bucket_id=1)

        rv = item.get_all_buckets_with_limit(bucket_id=1, limit=2)
        self.assertEquals(len(rv), 2)

    def test_limit_query_in_bucketlists(self):
        bucket.create_bucketlist(bucket_name='Journey to the moon',
                                 bucket_description='use a rocket to fly', user_id=1)
        item.create_bucketlistitem(item_name='Journey to the usa',
                                   item_status='pending',
                                   due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the japan',
                                   item_status='pending',
                                   due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='use a road to travel',
                                   due_date='12-08-2019', bucket_id=1)

        rv = item.get_all_buckets_with_search_limit(
            q="Journey to the japan", limit=2, bucket_id=1)
        self.assertEquals(len(rv), 1)


    # def test_update_bucketlistitems(self):
    #     bucket.create_bucketlist(bucket_name='Journey to the moon',
    #                              bucket_description='use a rocket to fly', user_id=1)
    #     item.create_bucketlistitem(item_name='Journey to the Africa',
    #                                item_status='pending',
    #                                due_date='12-08-2019', bucket_id=1)
    #     item.update_item(item_name='trip to china',
    #                      item_status='done',
    #                      due_date='12-03-2007',
    #                      bucket_id=1)
    #     rv = item.get_item_by_id(0, 1)
    #     print(rv)
    #     self.assertEqual(rv[0].get('item_name'), 'Journey to the Africa')

    def test_empty_item_name(self):
        bucket.create_bucketlist(bucket_name='Journey to the moon',
                                 bucket_description='use a rocket to fly', user_id=1)
        rv = item.create_bucketlistitem(item_name='',
                                        item_status='pending',
                                        due_date='12-08-2019',
                                        bucket_id=1)
        self.assertEqual(rv, 'All fields are required')

    def test_invalid_item_update(self):
        bucket.create_bucketlist(bucket_name='Journey to the moon',
                                 bucket_description='use a rocket to fly', user_id=1)
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='pending',
                                   due_date='12-08-2019',
                                   bucket_id=1)
        rv = item.update_item(item_name='trip to china',
                              item_status='done',
                              due_date='12-03-2007',
                              bucket_id=2)
        self.assertEqual(rv, 'Bucketlist item does not exist')

    def tearDown(self):
        super(BucketItemsTestCase, self).tearDown()
