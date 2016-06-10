from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading

import pytest
from webtest import TestApp

from tryiiif.app import create_app
from tryiiif.config import TestConfig


@pytest.yield_fixture(scope="session")
def iiif_server():
    address = ('localhost', 0)
    httpd = TCPServer(address, SimpleHTTPRequestHandler)
    t = threading.Thread(target=httpd.serve_forever)
    t.start()
    yield httpd.server_address
    httpd.shutdown()
    t.join()


@pytest.yield_fixture
def app(iiif_server):
    app = create_app(TestConfig)
    app.config['IIIF_SERVICE_URL'] = \
        "http://{}:{}/tests/fixtures/iiif/2".format(*iiif_server)
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def testapp(app):
    return TestApp(app)
