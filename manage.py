from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models.models import app
from app.models.models import db
from app.models.models import migrate
from app.models.models import User
from app.models.models import Bucketlist
# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bucketlist.db'

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()