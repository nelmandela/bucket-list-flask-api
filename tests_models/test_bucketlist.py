#!flask/bin/python
import unittest
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from app.models.models import db
from tests_models.base import BaseTest
from app.models.bucket_controller import BucketStore

bucket = BucketStore()


class BucketTestCase(BaseTest):
    def setUp(self):
        super(BucketTestCase, self).setUp()

    def test_create_bucketlist(self):
        response = bucket.create_bucketlist(bucket_name='Journey to the moon',
                                            bucket_description='use a rocket to fly', user_id=1)
        assert response == 'Bucket successfully added to user.'

    def test_get_bucketlist_by_id(self):
        bucket.create_bucketlist(bucket_name='Journey to the moon',
                                 bucket_description='use a rocket to fly', user_id=1)
        buckets = bucket.get_bucket_list_by_id(1)
        assert buckets[0].get("bucket_name") == 'Journey to the moon'

    def test_pagination_in_bucketlists(self):
        bucket.create_bucketlist(bucket_name='Journey to the usa',
                                 bucket_description='use a aeroplane to travel', user_id=1)
        bucket.create_bucketlist(bucket_name='Journey to the japan',
                                 bucket_description='use a rocket to travel', user_id=1)
        bucket.create_bucketlist(bucket_name='Journey to the Africa',
                                 bucket_description='use a road to travel', user_id=1)

        response = bucket.get_all_buckets_with_limit(limit=2, user_id=1)
        assert len(response) == 2

    def test_limit_query_in_bucketlists(self):
        bucket.create_bucketlist(bucket_name='trip to the usa',
                                 bucket_description='use a aeroplane to travel', user_id=1)
        bucket.create_bucketlist(bucket_name='Journey to the japan',
                                 bucket_description='use a rocket to travel', user_id=1)
        bucket.create_bucketlist(bucket_name='Journey to the Africa',
                                 bucket_description='use a road to travel', user_id=1)

        response = bucket.get_all_buckets_with_limit_query(
            q="Journey to the japan", limit=2, user_id=1)
        assert len(response) == 1

    def test_delete_bucketlists(self):
        bucket.create_bucketlist(bucket_name='trip to the usa',
                                 bucket_description='use a aeroplane to travel', user_id=1)
        bucket.create_bucketlist(bucket_name='Journey to the japan',
                                 bucket_description='use a rocket to travel', user_id=1)
        bucket.create_bucketlist(bucket_name='Journey to the Africa',
                                 bucket_description='use a road to travel', user_id=1)

        bucket.delete(1)
        response = bucket.get_all_buckets_with_limit(limit=1000, user_id=1)
        assert len(response) == 2

    def test_update_bucketlists(self):
        bucket.create_bucketlist(bucket_name='trip to the usa',
                                 bucket_description='use a aeroplane to travel', user_id=1)

        bucket.update(bucket_name='trip to china',
                      bucket_description='use a train', bucket_id=1)
        response = bucket.get_bucket_list_by_id(1)
        assert response[0].get('bucket_name') == 'trip to china'

    def test_empty_bucket_name(self):
        response = bucket.create_bucketlist(bucket_name='',
                                            bucket_description='use a aeroplane to travel', user_id=1)

        assert(response == 'All fields are required')

    def test_invalid_item_update(self):
        bucket.create_bucketlist(bucket_name='trip to the usa',
                                 bucket_description='use a aeroplane to travel', user_id=1)

        response = bucket.update(bucket_name='trip to china',
                                 bucket_description='use a train', bucket_id=2)
        assert response == False

    def test_no_duplicates_in_bucketlists(self):
        bucket.create_bucketlist(bucket_name='trip to china',
                                 bucket_description='use a aeroplane to travel', user_id=1)

        response = bucket.create_bucketlist(bucket_name='trip to china',
                                            bucket_description='use a train', bucket_id=2)
        assert response == 'Bucket not created'

    def tearDown(self):
        super(BucketTestCase, self).tearDown()
