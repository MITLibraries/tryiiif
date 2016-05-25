# -*- coding: utf-8 -*-
from __future__ import absolute_import
import base64
import uuid

from flask import (Blueprint, current_app, json, redirect, render_template,
                   request, url_for)
import requests
from werkzeug.urls import url_parse

from tryiiif.extensions import rc


home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    parts = url_parse(request.url_root)
    current_app.config.update(SERVER_NAME=parts.netloc,
                              SERVER_PROTOCOL=parts.scheme)
    if request.method == 'POST':
        url = request.form['url']
        name = request.form.get('title', url)
        b64url = base64.urlsafe_b64encode(url)
        uid = uuid.uuid4()
        iiif_url = current_app.config.get('IIIF_SERVICE_URL').rstrip('/')
        res = requests.get('{}/{}/info.json'.format(iiif_url, b64url))
        info = res.json()
        manifest = make_manifest(uid, url, b64url, name, info['height'],
                                 info['width'])
        rc.conn.set(uid, json.dumps(manifest))

        if request.form['submit'] in current_app.config['VIEWERS']:
            return redirect(url_for('viewers.viewer',
                                    viewer=request.form['submit'], uid=uid))
            
    return render_template('index.html')


def make_manifest(uid, url, iiifid, name, height, width):
    proto = current_app.config.get('SERVER_PROTOCOL')
    manifest_url = url_for('iiif.manifest', uid=uid, _external=True,
                           _scheme=proto)
    sequence_url = url_for('iiif.sequence', uid=uid, _external=True,
                           _scheme=proto)
    canvas_url = url_for('iiif.canvas', uid=uid, _external=True,
                         _scheme=proto)
    iiif_svc_url = '{}/{}'.format(
        current_app.config.get('IIIF_SERVICE_URL').rstrip('/'), iiifid)
    return {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": manifest_url,
        "label": name,
        "attribution": "Provided by TryIIF from {}".format(url),
        "sequences": [{
            "@id": sequence_url,
            "@type": "sc:Sequence",
            "label": "Current Page Order",
            "canvases": [{
                "@id": canvas_url,
                "@type": "sc:Canvas",
                "label": name,
                "height": int(height),
                "width": int(width),
                "images": [{
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "on": canvas_url,
                    "resource": {
                        "@id": url,
                        "@type": "dctypes:Image",
                        "format": "image/{}".format(url.split('.')[-1]),
                        "height": int(height),
                        "width": int(width),
                        "service": {
                            "@context": "http://iiif.io/api/image/2/context.json",
                            "@id": iiif_svc_url,
                            "profile": "http://iiif.io/api/image/2/level1.json"
                        }
                    }
                }]
            }]
        }]
    }
