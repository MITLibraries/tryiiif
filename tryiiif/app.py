# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask

from tryiiif.extensions import rc
from tryiiif.home import home
from tryiiif.iiif import iiif


def create_app(cfg=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(cfg)
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    app.register_blueprint(home)
    app.register_blueprint(iiif, url_prefix='/iiif')


def register_extensions(app):
    rc.init_app(app)
