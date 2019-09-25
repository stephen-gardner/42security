from flask import Blueprint

bp = Blueprint("watchlist", __name__)

from app.watchlist import routes
