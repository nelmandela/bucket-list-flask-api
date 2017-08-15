# bucket-list-flask-api

[![Build Status](https://travis-ci.org/jmnyarega/bucket_list_app.svg?branch=master)](https://travis-ci.org/jmnyarega/bucket_list_app)
[![Coverage Status](https://coveralls.io/repos/github/jmnyarega/bucket-list-flask-api/badge.svg?branch=master)](https://coveralls.io/github/jmnyarega/bucket-list-flask-api?branch=master)

## What the bucketlist api does
Allows users  to record and share things they want to achieve or experience before reaching a certain age, meeting the needs of, keeping track of their dreams and goals.

## Endpoints

| Methods | endpoints | Description  |
| --- | --- | --- |
| POST | `/auth/login`  | logs in  a user.
| POST | `/auth/register`  | registers a new user
| POST | `/bucketlists/`  | Adds a bucket list.
| GET | `/bucketlists/`   | gets all the created bucket lists.
| GET | `/bucketlists/<bucket_id>`  | Get one bucket list by id. 
| PUT | `/bucketlists/<bucket_id>`  | Update one bucket list by id. 
| DELETE |  `/bucketlists/<bucket_id>`  | Delete one bucket list by id. 
| POST | `/bucketlist/<bucket_id>/items/`  | Add a new item to this bucket list.
| PUT | `/bucketlist/<bucket_id>/item/<item_id>/`  | Update one bucket list by id.             
| DELETE | `/bucketlists/<bucket_id>/items/<item_id>` |  Delete one bucketlist item list by id. 
| POST   |`/sharebucketlist/<bucket_id>/<user_id>` |  Shares a bucketlist to another user. 


## INSTALLATION & SET UP.

1. Clone the project on github: 

2. Checkout to develop branch

3. Create a ***virtual environment*** and start the virtual environment

4. Install the dependencies via ```pip install -r requirements.txt```


## Run the Migrations:

1. ```python manage.py db init```

2. ```python manage.py db migrate```

3. ```python manage.py db upgrade```

> The server should be running on [http://127.0.0.1:5000] 

## Testing the api:

``` change directory to root ```
``` and the run ` pytest` ```
