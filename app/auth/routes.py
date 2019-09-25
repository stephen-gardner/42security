from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

import ldap

from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if not form.validate_on_submit():
        return render_template("auth/login.html", title="Sign In", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
        try:
            ldap.set_option(ldap.OPT_REFERRALS, 0)
            ldap.protocol_version = 3
            conn = ldap.initialize("ldap://dc-staff.42.us.org")
            conn.simple_bind_s(form.username.data + "@staff.42.us.org", form.password.data)
            user = User().query.limit(1).all()[0]
        except ldap.LDAPError:
            flash("Invalid username or password", "danger")
            return redirect(url_for(".login"))

    login_user(user, remember=form.remember_me.data)

    next_page = request.args.get("next")
    # if next is not specified, or points to a non-relative path, the user is forwarded to the index
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for("main.index")
    return redirect(next_page)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
