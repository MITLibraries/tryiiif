# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask.ext.cors import CORS

from tryiiif.extensions import rc
from tryiiif.home import home
from tryiiif.iiif import iiif
from tryiiif.viewers import viewers


def create_app(cfg=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(cfg)
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    app.register_blueprint(home)
    app.register_blueprint(iiif, url_prefix='/iiif')
    app.register_blueprint(viewers, url_prefix='/viewer')


def register_extensions(app):
    rc.init_app(app)
    CORS(app)
