from flask import current_app, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask_login import login_required

import os

from app import db, photos
from app.models import StaffMember
from app.staff import bp
from app.staff.forms import AddStaffForm
from app.util import hash_rename


@bp.route("/")
@login_required
def stafflist():
    return render_template(
        "lists/staff.html",
        staff_members=StaffMember.query.filter_by(visible=True), form=AddStaffForm(), photos=photos, title="Staff"
    )


@bp.route("/add", methods=["POST"])
@login_required
def add_to_staff():
    form = AddStaffForm()
    if not form.validate_on_submit():
        for _, errors in form.errors.items():
            for msg in errors:
                flash(msg, "danger")
        return redirect(url_for(".stafflist"))

    photo_name = hash_rename(photos, photos.save(form.photo.data))
    sm = StaffMember(
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        photo=photo_name,
        role=form.role.data,
        slack=form.slack.data,
        phone=form.phone.data,
        email=form.email.data
    )
    db.session.add(sm)
    db.session.commit()
    flash(Markup("<strong>%s %s</strong> has been added to staff." % (sm.first_name, sm.last_name)), "success")
    return redirect(url_for(".stafflist"))


@bp.route("/remove/<id>")
@login_required
def remove_from_staff(id):
    sm = StaffMember.query.filter_by(id=id).first()

    if sm is not None:
        sm.visible = False
        db.session.commit()
        flash(Markup("<strong>%s %s</strong> has been removed from staff." % (sm.first_name, sm.last_name)), "success")
    else:
        flash("User specified could not be found.", "danger")

    return redirect(url_for(".stafflist"))


@bp.route("/edit/firstName", methods=["POST"])
@login_required
def edit_first_name():
    sm = StaffMember.query.filter_by(id=request.form.get("pk")).first()
    sm.first_name = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)


@bp.route("/edit/lastName", methods=["POST"])
@login_required
def edit_last_name():
    sm = StaffMember.query.filter_by(id=request.form.get("pk")).first()
    sm.last_name = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)


@bp.route("/edit/role", methods=["POST"])
@login_required
def edit_role():
    sm = StaffMember.query.filter_by(id=request.form.get("pk")).first()
    sm.role = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)


@bp.route("/edit/slack", methods=["POST"])
@login_required
def edit_slack():
    sm = StaffMember.query.filter_by(id=request.form.get("pk")).first()
    sm.slack = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)


@bp.route("/edit/phone", methods=["POST"])
@login_required
def edit_phone():
    sm = StaffMember.query.filter_by(id=request.form.get("pk")).first()
    sm.phone = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)


@bp.route("/edit/email", methods=["POST"])
@login_required
def edit_email():
    sm = StaffMember.query.filter_by(id=request.form.get("pk")).first()
    sm.email = request.form.get("value")
    db.session.commit()
    return jsonify(success=True)
