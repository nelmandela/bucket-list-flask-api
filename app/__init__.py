import os
import sys

from flask import Flask
# Add top-level directory to module search path.
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
app = Flask(__name__)   
app.config.from_object('config.DevelopmentConfig')

