import pytest

from webtest import TestApp

from tryiiif.app import create_app
from tryiiif.config import TestConfig


@pytest.yield_fixture
def app():
    app = create_app(TestConfig)
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def testapp(app):
    return TestApp(app)
