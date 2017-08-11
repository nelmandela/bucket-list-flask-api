
from flask_script import Manager
from flask_migrate import  MigrateCommand
from app.view import *


manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    """Runs the unit tests without test coverage."""
    app.run(debug=True)


if __name__ == '__main__':
    manager.run()
