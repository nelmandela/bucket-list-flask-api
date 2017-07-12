from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bucketlist.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    buckets = db.relationship('Bucketlist', backref='user',
                                lazy='dynamic')


class Bucketlist(db.Model):
    bucket_id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String)
    bucket_descriptions = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('BucketlistItems', backref='bucketlist',
                                lazy='dynamic')

class BucketlistItems(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)
    item_status = db.Column(db.String)
    due_date    = db.Column(db.String)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlist.bucket_id'))  