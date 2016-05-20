# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import abort, Blueprint, request, render_template, url_for

from tryiiif.extensions import rc


viewers = Blueprint('viewers', __name__)


@viewers.route('/<viewer>/<uid>')
def viewer(viewer, uid):
    if viewer not in ['uv']:
        abort(404)
    manifest = url_for('iiif.manifest', uid=uid)
    return render_template('viewers/{}.html'.format(viewer), manifest=manifest)
