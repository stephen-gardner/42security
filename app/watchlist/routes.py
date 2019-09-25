from flask import flash, jsonify, Markup, redirect, render_template, request, url_for
from flask_login import login_required

from app import db, photos
from app.intra import get_user_info
from app.models import BannedUser
from app.util import hash_rename
from app.watchlist import bp
from app.watchlist.forms import BanUserForm


@bp.route("/")
@login_required
def watchlist():
    return render_template(
        "lists/watchlist.html",
        banned=BannedUser.query.filter_by(visible=True), form=BanUserForm(), photos=photos, title="Watchlist"
    )


@bp.route("/add", methods=["POST"])
@login_required
def add_to_watchlist():
    form = BanUserForm()
    if not form.validate_on_submit():
        for _, errors in form.errors.items():
            for msg in errors:
                flash(msg, "danger")
        return redirect(url_for(".watchlist"))

    intra_id = form.intra_id.data
    user_info = None

    if form.photo.has_file():
        photo_name = photos.save(form.photo.data)
    else:
        user_info = get_user_info(intra_id, save_photo=True)
        photo_name = None if user_info is None else user_info.get("photo_name")

    if photo_name is not None:
        photo_name = hash_rename(photos, photo_name)

    no_first = len(form.first_name.data) == 0
    no_last = len(form.last_name.data) == 0

    if user_info is None and (no_first or no_last):
        user_info = get_user_info(intra_id, save_photo=False)
        if user_info is None:
            flash(Markup(
                "Unable to find intra user <strong>%s</strong>. "
                "First and last name must be specified." % intra_id
            ), "danger")
            return redirect(url_for(".watchlist"))

    bu = BannedUser(
        intra_id=intra_id,
        first_name=user_info.get("first_name") if no_first else form.first_name.data,
        last_name=user_info.get("last_name") if no_last else form.last_name.data,
        reason=form.reason.data,
        photo=photo_name
    )
    db.session.add(bu)
    db.session.commit()
    flash(Markup("<strong>%s</strong> has been added to the watchlist." % intra_id), "success")
    return redirect(url_for(".watchlist"))


@bp.route("/remove/<id>")
@login_required
def remove_from_watchlist(id):
    bu = BannedUser.query.filter_by(id=id).first()

    if bu is not None:
        bu.visible = False
        db.session.commit()
        flash(Markup("<strong>%s</strong> has been removed from the watchlist." % bu.intra_id), "success")
    else:
        flash(Markup("<strong>%s</strong> is not on the watchlist." % bu.intra_id), "danger")

    return redirect(url_for(".watchlist"))


@bp.route("/edit/firstName", methods=["POST"])
@login_required
def edit_first_name():
    bu = BannedUser.query.filter_by(id=request.form.get("pk")).first()
    bu.first_name = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)


@bp.route("/edit/lastName", methods=["POST"])
@login_required
def edit_last_name():
    bu = BannedUser.query.filter_by(id=request.form.get("pk")).first()
    bu.last_name = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)


@bp.route("/edit/reason", methods=["POST"])
@login_required
def edit_reason():
    bu = BannedUser.query.filter_by(id=request.form.get("pk")).first()
    bu.reason = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)
