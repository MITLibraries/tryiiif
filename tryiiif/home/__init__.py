# -*- coding: utf-8 -*-
from __future__ import absolute_import
from hashlib import sha1

from flask import (Blueprint, current_app, json, redirect, render_template,
                   request, url_for, flash, abort)
import requests
from werkzeug.urls import url_parse

from tryiiif.extensions import rc


home = Blueprint('home', __name__)


@home.before_request
def before_request():
    # yes, this is backward from what it seems like it should be.
    # However, for this demo app we are forcing http to prevent insecure
    # content restrictions for content from our image server that is currently
    # http-only.
    if request.url.startswith('https://'):
        url = request.url.replace('https://', 'http://', 1)
        code = 301
        return redirect(url, code=code)


@home.route('/', methods=['GET', 'POST'])
def index():
    parts = url_parse(request.url_root)
    current_app.config.update(SERVER_NAME=parts.netloc,
                              SERVER_PROTOCOL=parts.scheme)
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        name = request.form.get('title', url)
        viewer = request.form.get('submit')

        if url is None or url == '':
            flash('A URL to an image is required.', 'danger')
            return render_template('index.html')

        if viewer not in current_app.config['VIEWERS']:
            abort(404)

        h = sha1()
        h.update(url.encode('utf-8'))
        url_hash = h.hexdigest()
        rc.conn.set(url_hash, url)
        iiif_url = current_app.config.get('IIIF_SERVICE_URL').rstrip('/')
        res = requests.get('{}/{}/info.json'.format(iiif_url, url_hash))
        try:
            res.raise_for_status()
        except:
            hr = requests.head(url)
            if 400 <= hr.status_code < 500:
                flash('It looks like there\'s nothing there. Please double '
                      'check your URL.', 'danger')
                return render_template('index.html')
            elif not hr.headers.get('content-type', '').startswith('image'):
                flash('That doesn\'t look like an image. Please double check '
                      'your URL.', 'danger')
                return render_template('index.html')
            else:
                flash('Something went wrong. Please try again later.',
                      'danger')
                return render_template('index.html')

        info = res.json()
        manifest = make_manifest(url_hash, url, url_hash, name, info['height'],
                                 info['width'])
        rc.conn.set('manifest:{}'.format(url_hash), json.dumps(manifest))

        return redirect(url_for('viewers.viewer', viewer=viewer, uid=url_hash))
    return render_template('index.html')


@home.route('/url/<url_hash>', methods=['GET'])
def url(url_hash):
    url = rc.conn.get(url_hash)
    if url is None:
        abort(404)
    return url


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
        "attribution": "Provided by TryIIIF from {}".format(url),
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
