TryIIIF
=======

https://tryiiif.herokuapp.com

Develop
-------

After cloning the repo, use pip to install dependencies into a virtualenv::

  (tryiiif)$ pip install -r requirements.txt

Create a ``.env`` at the root of the repo with a few settings:

- ``REDISTOGO_URL``: Redis connection URL, for example ``redis://localhost:6379``
- ``IIIF_SERVICE_URL``: URL to the IIIF service. This should be the full URL, for example: ``http://example.com/iiif/2``

To run the app, you can use something like `honcho <https://github.com/nickstenning/honcho>`_ from the project root::

  (tryiiiif)$ honcho start
