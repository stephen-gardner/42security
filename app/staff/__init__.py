from flask import Blueprint

bp = Blueprint("staff", __name__)

from app.staff import routes
