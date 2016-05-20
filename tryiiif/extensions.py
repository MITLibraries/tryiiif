# -*- coding: utf-8 -*-
from __future__ import absolute_import

import redis


class RedisConnection(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conn = redis.from_url(app.config['REDISTOGO_URL'])


rc = RedisConnection()
