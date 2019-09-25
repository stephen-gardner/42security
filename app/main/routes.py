from flask import current_app, redirect, request, send_from_directory, url_for
from flask_login import login_required
from thumbnails import get_thumbnail

import os

from app.main import bp
from app.models import BannedUser, StaffMember


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return redirect(url_for("watchlist.watchlist"))


@bp.route("/static/photos/<img>")
def get_photo(img):
    photos_dir = current_app.config.get("UPLOADED_PHOTOS_DEST")
    use_thumb = request.args.get("thumb")
    img_path = os.path.join(photos_dir, img)

    if os.path.exists(img_path):
        if use_thumb:
            try:
                thumb = get_thumbnail(os.path.join(img_path), "x40")
                return send_from_directory("/", thumb.path.lstrip('/'))
            except IOError:  # images with alpha channels can't be converted by python-thumbnails
                pass
        else:
            return send_from_directory(photos_dir, img)

    return send_from_directory(photos_dir, "unknown_thumb.png" if use_thumb else "unknown.png")
