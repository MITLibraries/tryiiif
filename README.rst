.. image:: https://travis-ci.org/MITLibraries/tryiiif.svg?branch=master
    :target: https://travis-ci.org/MITLibraries/tryiiif
    :alt: Build Status
.. image:: https://www.versioneye.com/user/projects/575b06935758a9000de9a25e/badge.svg?style=flat
    :target: https://www.versioneye.com/user/projects/575b06935758a9000de9a25e
    :alt: Dependency Status
.. image:: https://img.shields.io/badge/license-Apache%20License%202.0-blue.svg
    :target: https://raw.githubusercontent.com/MITLibraries/tryiiif/master/LICENSE.txt
    :alt: Apache 2 licensed

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

Use ``tox`` to run the tests. The test suite requires a running instance of redis. By default, it will look for this instance at ``redis://localhost:6379``. If it is running at a different URL pass it as the ``REDISTOGO_URL`` env variable to  ``tox``. For example::

    $ REDISTOGO_URL='redis://localhost:9999' tox
