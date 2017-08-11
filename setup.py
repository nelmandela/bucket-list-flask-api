from distutils.core import setup

setup(
    name='bucket-list-flask-api',
    version='1.0',
    packages=['flask',
              'alembic',
              'gunicorn',
              'psycopg2',
              'flask_jwt',
              'flask_cors',
              'flask_restplus',
              'flask_sqlalchemy',
              'sqlalchemy_paginator',
              'flask_restful_swagger'],
    url='',
    license='',
    author='Josiah Nyarega',
    author_email='josiah.mokobo@andela.com',
    description='bucketlist api '
)
