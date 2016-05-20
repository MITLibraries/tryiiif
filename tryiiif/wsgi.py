from tryiiif.app import create_app
from tryiiif.config import Heroku


application = create_app(Heroku)
