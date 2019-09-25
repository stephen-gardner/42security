from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)

    def __repr__(self):
        return "<User | %s>" % self.username

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class BannedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intra_id = db.Column(db.String, index=True)
    first_name = db.Column(db.String, index=True)
    last_name = db.Column(db.String, index=True)
    reason = db.Column(db.String)
    photo = db.Column(db.String)
    visible = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<BannedUser | %s (%s %s)>" % (self.intra_id, self.first_name, self.last_name)


class StaffMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, index=True)
    last_name = db.Column(db.String, index=True)
    role = db.Column(db.String, index=True)
    slack = db.Column(db.String, index=True)
    phone = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True)
    photo = db.Column(db.String)
    visible = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<StaffMember | %s %s (%s)>" % (self.first_name, self.last_name, self.role)


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))
