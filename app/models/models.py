from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    buckets = db.relationship('Bucketlist', backref='user',
                              lazy='dynamic')

    def __init__(self, name, username, email, password):
        self.username = username
        self.email = email
        self.name = name
        self.password = password
        # self.public_id = public_id

    def __repr__(self):
        return '<User %r>' % self.username



class Bucketlist(db.Model):
    bucket_id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String)
    bucket_descriptions = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('BucketlistItems', backref='bucketlist',
                            lazy='dynamic')

    def __init__(self, bucket_name, bucket_descriptions, user_id):
        self.bucket_name = bucket_name
        self.bucket_descriptions = bucket_descriptions
        self.user_id = user_id

    def __repr__(self):
        return '<Bucketlist %r>' % self.bucket_name


class BucketlistItems(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, unique=True)
    item_status = db.Column(db.String)
    due_date = db.Column(db.String)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlist.bucket_id'))

    def __init__(self, item_name, item_status, due_date,  bucket_id):
        self.item_name = item_name
        self.item_status = item_status
        self.due_date = due_date
        self.bucket_id = bucket_id

    def __repr__(self):
        return '<BucketlistItems %r>' % self.item_name
