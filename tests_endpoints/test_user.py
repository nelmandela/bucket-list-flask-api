import json
from tests_endpoints.base_testcase import BaseTest


class TestCaseBucketItems(BaseTest):
    def setUp(self):
        super(TestCaseBucketItems, self).setUp()

        self.user = dict(name="josiah", username="mathew",
                         email="josiah@gmail.com", password_hash="jacob")

    def header_with_no_authetication(self):
        return {"Content-Type": "application/json"}

    def tearDown(self):
        super(TestCaseBucketItems, self).tearDown()

    def test_create_user(self):
        # create a new user
        rv = self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(self.user))

        self.assertEqual(json.loads(rv.data.decode()), {
                         "message": "User successfully created."})

    def test_register_with_invalid_email(self):
        # create a new user
        self.user = dict(name="josiah", username="james",
                         email="j@gmail.#com", password_hash="jacob")
        rv = self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(self.user))

        self.assertEqual(json.loads(rv.data.decode()), {
                         "message": "invalid email address"})

    def test_register_with_empty_email_field(self):
        # create a new user
        self.user = dict(name="josiah", username="james",
                         email="", password_hash="jacob")
        rv = self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(self.user))

        self.assertEqual(json.loads(rv.data.decode()), {
                         'message': 'All fields are required'})


    def test_register_with_existing_email(self):
        # create a new user
        self.user = dict(name="josiahs", username="joshy",
                         email="mary@gmail.com", password_hash="jacob")
        self.user2 = dict(name="marks", username="jimmy",
                          email="mary@gmail.com", password_hash="jacob")
        # register first user
        self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(self.user))

        # register second user
        rv = self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(self.user2))


        self.assertEqual(json.loads(rv.data.decode()), {
                         "message": "email already exists."})

    def test_register_with_existing_username(self):
        # create a new user
        self.user = dict(name="josephat", username="james",
                         email="test@gmail.com", password_hash="jacob")
        self.user2 = dict(name="josephat", username="james",
                          email="test_dups@gmail.com", password_hash="jacob")
        # register first user
        self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(self.user))

        # register second user
        rv = self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(self.user2))

        self.assertEqual(json.loads(rv.data.decode()), {
                         "message": "username already exists."})

    def test_login_with_invalid_credentials(self):
        # create a new user
        user = dict(username="josiah", password_hash="flask")

        # login user
        rv = self.client.post(
            '/auth/login', headers=self.header_with_no_authetication(), data=json.dumps(user))
        self.assertEqual(json.loads(rv.data.decode()), {
            "description": "Invalid credentials",
            "error": "Bad Request",
            "status_code": 401
        })

    def test_login_with_valid_credentials(self):
        # user details
        user_details = dict(name="josephat", username="james",
                            email="test_dups@gmail.com", password_hash="jacob")

        # register user
        self.client.post(
            '/auth/register/', headers=self.header_with_no_authetication(), data=json.dumps(user_details))

        # login user
        rv = self.client.post(
            '/auth/login',
            data=json.dumps(dict(
                username='james',
                password='jacob'
            )),
            content_type='application/json'
        )

        self.assertIsNotNone(json.loads(rv.data.decode())['access_token'])

    def test_access_resource_without_token(self):
        rv = self.client.get(
            '/bucketlists/', headers=self.header_with_no_authetication())
        self.assertEqual(rv._status_code, 401)

    def test_access_resource_with_token(self):

        rv = self.client.get(
            '/bucketlists/', headers=self.set_header())
        self.assertEqual(rv._status_code, 404)
