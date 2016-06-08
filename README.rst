TryIIIF
=======

http://tryiiif.herokuapp.com

Develop
-------

After cloning the repo, use pip to install dependencies into a virtualenv::

  (tryiiif)$ pip install -r requirements.txt

Create a ``.env`` at the root of the repo with a few settings:

- ``REDISTOGO_URL``: Redis connection URL, for example ``redis://localhost:6379``
- ``IIIF_SERVICE_URL``: URL to the IIIF service. This should be the full URL, for example: ``http://example.com/iiif/2``
- ``ROLLBAR_TOKEN``: Optional https://rollbar.com token for exception logging
- ``FLASK_ENV``: Optional string to identify where flask is running, for example ``production``
- ``SECRET_KEY``: Optional string to set a session secret key. This should be set in production environments. Information on how to generate and what this does here: http://flask.pocoo.org/docs/0.11/quickstart/#sessions

To run the app, you can use something like `honcho <https://github.com/nickstenning/honcho>`_ from the project root::

  (tryiiiif)$ honcho start


Running Tests
-------------
`pip install tox`
`IIIF_SERVICE_URL=http://127.0.0.1:8182/iiif/2 REDISTOGO_URL='' tox`
