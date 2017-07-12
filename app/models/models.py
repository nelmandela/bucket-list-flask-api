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

class Bucketlist(db.Model):
    bucket_id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String)
    bucket_descriptions = db.Column(db.String)