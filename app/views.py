from flask import render_template, request, redirect, Flask
from flask import url_for, session
from werkzeug.security import generate_password_hash

from app import app

@app.route('/auth/login', methods=['POST'])
def login():
    return ""


@app.route('/auth/register', methods=['POST'])
def register():
    return ""

@app.route('/bucketlists', methods=['POST'])
def bucketlists():
    return ""

@app.route('/bucketlists', methods=['POST'])
def bucketlists():
    return ""

@app.route('/bucketlists', methods=['GET'])
def bucketlists():
    return ""

@app.route('/bucketlists/<int:bucket_id>', methods=['GET'])
def bucketlists():
    return ""

@app.route('/bucketlists/<int:id>', methods=['PUT'])
def bucketlists():
    return ""

@app.route('/bucketlists/<int:bucket_id>', methods=['DELETE'])
def bucketlists():
    return ""

@app.route('/bucketlists/<int:bucket_id>/items', methods=['POST'])
def bucketlists():
    return ""

@app.route('/bucketlists/<int:bucket_id>/items/<int:item_id>', methods=['POST'])
def bucketlists():
    return ""

@app.route('/bucketlists/<int:bucket_id>/items/<int:item_id>', methods=['DELETE'])
def bucketlists():
    return ""
