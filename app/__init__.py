import os
import sys
import config

from flask import Flask
# Add top-level directory to module search path.
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

