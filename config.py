import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    INTRA_UID = os.environ.get("INTRA_UID")
    INTRA_SECRET = os.environ.get("INTRA_SECRET")
    INTRA_TOKEN_URL = "https://api.intra.42.fr/oauth/token"
    MAX_PHOTO_SIZE = 2 * 1024 * 1024  # 2 MB
    SECRET_KEY = os.environ.get("SECRET_KEY") or "5qQBnIh3FTeAaycEKse5"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "security.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, "static/photos")
    UPLOADED_PHOTOS_URL = "/static/photos/"
