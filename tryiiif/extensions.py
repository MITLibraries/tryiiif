# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import redis
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception


class RedisConnection(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conn = redis.from_url(app.config['REDISTOGO_URL'])


rc = RedisConnection()


class RollbarConnection:
    def init_rollbar(self, app):
        rollbar.init(
            app.config['ROLLBAR_TOKEN'],
            app.config['FLASK_ENV'],
            root=os.path.dirname(os.path.realpath(__file__)),
            allow_logging_basic_config=False)

        got_request_exception.connect(
            rollbar.contrib.flask.report_exception, app)


rb = RollbarConnection()
