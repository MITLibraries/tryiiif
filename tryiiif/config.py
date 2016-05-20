import os 


class Default(object):
    DEBUG = True
    TESTING = False


class Heroku(Default):
    REDISTOGO_URL = os.environ['REDISTOGO_URL']
    IIIF_SERVICE_URL = os.environ['IIIF_SERVICE_URL']
