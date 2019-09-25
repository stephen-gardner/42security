from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

from app import photos


class AddStaffForm(FlaskForm):
    first_name = StringField("First Name<span class=\"text-danger\">*</span>", validators=[DataRequired()])
    last_name = StringField("Last Name<span class=\"text-danger\">*</span>", validators=[DataRequired()])
    photo = FileField("Photo<span class=\"text-danger\">*</span>", validators=[FileAllowed(photos), FileRequired()])
    role = StringField("Role<span class=\"text-danger\">*</span>", validators=[DataRequired()])
    slack = StringField("Slack ID")
    phone = StringField("Phone")
    email = StringField("Email")
    submit = SubmitField("Add User")
