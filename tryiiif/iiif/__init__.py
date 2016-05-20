# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import abort, Blueprint, json

from tryiiif.extensions import rc


iiif = Blueprint('iiif', __name__)


@iiif.route('/<uid>/manifest')
def manifest(uid):
    return json.jsonify(json.loads(rc.conn.get(uid)))


@iiif.route('/<uid>/sequence/normal')
def sequence(uid):
    abort(404)


@iiif.route('/<uid>/canvas/p1')
def canvas(uid):
    abort(404)
