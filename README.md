# bucketlist-api

[![Build Status](https://travis-ci.org/jmnyarega/bucket_list_app.svg?branch=master)](https://travis-ci.org/jmnyarega/bucket_list_app)
[![Coverage Status](https://coveralls.io/repos/github/jmnyarega/bucket-list-flask-api/badge.svg?branch=master)](https://coveralls.io/github/jmnyarega/bucket-list-flask-api?branch=master)

## What the bucketlist api does
Allows users  to record and share things they want to achieve or experience before reaching a certain age, meeting the needs of, keeping track of their dreams and goals.

## Online link (heroku)

- https://bucketlist-apis-staging.herokuapp.com

## Endpoints

|  Endpoints | Description  | Public Access |
| --- | :--- | ---: |
| POST  `/auth/login`  | logs in  a user. | TRUE
| POST  `/auth/register`  | registers a new user | TRUE
| POST  `/bucketlists/`  | Adds a bucket list.| FALSE
| GET  `/bucketlists/`   | gets all the created bucket lists.| FALSE
| GET  `/bucketlists/<bucket_id>`  | Get one bucket list by id. | FALSE
| PUT  `/bucketlists/<bucket_id>`  | Update one bucket list by id. | FALSE
| DELETE   `/bucketlists/<bucket_id>`  | Delete one bucket list by id. | FALSE
| POST  `/bucketlist/<bucket_id>/items/`  | Add a new item to this bucket list.| FALSE
| PUT  `/bucketlist/<bucket_id>/item/<item_id>/`  | Update one bucket list by id.   | FALSE          
| DELETE  `/bucketlists/<bucket_id>/items/<item_id>` |  Delete one bucketlist item list by id. | FALSE
| POST  `/sharebucketlist/<bucket_id>/<user_id>` |  Shares a bucketlist to another user. | FALSE

- API pagination example: 

    _`http://localhost:5000/bucketlists?limit=20`_

- API searching example: 

    _`http://localhost:5000/bucketlists?q=bucket1`_


## Installation.

1. Clone the project on github: 

2. Checkout to develop branch

3. Create a `virtual environment` 

4. Activate the virtual environment

5. Install the dependencies via `pip install -r requirements.txt`

## Setting up Database

- Use Posgres to setup your database
- Create database with name   `bucket`

## Run the Migrations:

1. _python  manage.py db init_

2. _python  manage.py db migrate_

3. _python  manage.py db upgrade_

## Starting the server
- On the root directory, run `python manage.py runserver`

>> **The server should be running on [http://127.0.0.1:5000]**


## Testing the api:

- On the root directory, run ` pytest`
