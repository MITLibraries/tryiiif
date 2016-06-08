import os


class Default(object):
    DEBUG = True
    TESTING = False
    VIEWERS = ['uv', 'mirador']


class Heroku(Default):
    REDISTOGO_URL = os.environ['REDISTOGO_URL']
    IIIF_SERVICE_URL = os.environ['IIIF_SERVICE_URL']
    ROLLBAR_TOKEN = os.environ.get('ROLLBAR_TOKEN')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')


class TestConfig(Default):
    TESTING = True
    DEBUG = False
    REDISTOGO_URL = 'redis://localhost:6379'
    IIIF_SERVICE_URL = os.environ['IIIF_SERVICE_URL']
    FLASK_ENV = 'test'
    ROLLBAR_TOKEN = None
    SECRET_KEY = 'super_secret'
