import os 


class Default(object):
    DEBUG = True
    TESTING = False


class Heroku(Default):
    SERVER_NAME = os.environ['SERVER_NAME']
    SERVER_PROTOCOL = os.environ['SERVER_PROTOCOL']
    REDISTOGO_URL = os.environ['REDISTOGO_URL']
    IIIF_SERVICE_URL = os.environ['IIIF_SERVICE_URL']
