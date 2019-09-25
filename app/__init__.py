from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, IMAGES, patch_request_class, UploadSet

import logging
from logging.handlers import RotatingFileHandler
import os

from config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
login.login_view = "auth.login"
moment = Moment()
photos = UploadSet("photos", IMAGES)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    patch_request_class(app, app.config.get("MAX_PHOTO_SIZE"))
    configure_uploads(app, photos)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.staff import bp as staff_bp
    app.register_blueprint(staff_bp, url_prefix="/staff")
    from app.watchlist import bp as watchlist_bp
    app.register_blueprint(watchlist_bp, url_prefix="/watchlist")

    if not app.debug:
        if not os.path.exists("logs"):
            os.mkdir("logs")

        file_handler = RotatingFileHandler("logs/security.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: "
            "%(message)s [in %(pathname)s:%(lineno)d]"
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Security app startup")

    return app


from app import models
