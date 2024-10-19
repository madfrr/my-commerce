# from .cors import CORS
from .authentication import auth


def setup_middlewares(app):
    # CORS(app)
    auth(app)