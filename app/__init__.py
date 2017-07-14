import os
import sys

from flask import Flask
# Add top-level directory to module search path.
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bucket'
