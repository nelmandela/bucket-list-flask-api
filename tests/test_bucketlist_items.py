#!flask/bin/python
import unittest
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.items_controller import ItemStore
from app.models.models import *

from app.models.models import db
from app import app

item = ItemStore()


class BucketItemsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def test_create_bucket_item(self):
        response = item.create_bucketlistitem(item_name='Eat chinese food',
                                              item_status='pending',
                                              due_date='12-03-2017',
                                              bucket_id='1')

        assert response == 'Bucketlist item successfully added to user.'

    def test_get_bucketlist_by_id(self):
        item.create_bucketlistitem(item_name='Eat chinese food',
                                   item_status='pending',
                                   due_date='12-03-2017',
                                   bucket_id='1')

        items = item.get_item_by_id(1, 1)
        assert items[0].get("item_name") == 'Eat chinese food'

    def test_pagination_in_bucketlists_items(self):
        item.create_bucketlistitem(item_name='Journey to the usa',
                                   item_status='use a aeroplane to travel', due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the japan',
                                   item_status='use a rocket to travel', due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)

        response = item.get_all_buckets_with_limit(bucket_id=1, limit=2)
        assert len(response) == 2

    def test_limit_query_in_bucketlists(self):
        item.create_bucketlistitem(item_name='Journey to the usa',
                                   item_status='use a aeroplane to travel', due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the japan',
                                   item_status='use a rocket to travel', due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)

        response = item.get_all_buckets_with_search_limit(
            q="Journey to the japan", limit=2, bucket_id=1)
        assert len(response) == 1

    def test_delete_bucketlists(self):
        item.create_bucketlistitem(item_name='Journey to the usa',
                                   item_status='use a aeroplane to travel', due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the japan',
                                   item_status='use a rocket to travel', due_date='12-08-2019', bucket_id=1)
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)

        item.delete_item(1, 1)
        response = item.get_all_buckets_with_limit(limit=1000, bucket_id=1)
        assert len(response) == 2

    def test_update_bucketlistitems(self):
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)
        item.update_item(item_name='trip to china',
                         item_status='done',
                         due_date='12-03-2007',
                         bucket_id=1)
        response = item.get_item_by_id(1, 1)
        print(response[0].get('item_name'))
        assert response[0].get('item_name') == 'Journey to the Africa'

    def test_empty_item_name(self):
        response = item.create_bucketlistitem(item_name='',
                                              item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)
        assert(response == 'All fields are required')

    def test_invalid_item_update(self):
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)
        response = item.update_item(item_name='trip to china',
                                    item_status='done',
                                    due_date='12-03-2007',
                                    bucket_id=2)
        assert response == 'Bucketlist item does not exist'

    def test_no_duplicates_in_bucketlistsitems(self):
        item.create_bucketlistitem(item_name='Journey to the Africa',
                                   item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)

        response = item.create_bucketlistitem(item_name='Journey to the Africa',
                                              item_status='use a road to travel', due_date='12-08-2019', bucket_id=1)
        print(response)
        assert response == 'Item name already exists'

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        print("Destroying test database...")


if __name__ == '__main__':
    unittest.main()
