from flask import Markup
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp, ValidationError

from app import photos
from app.models import BannedUser


class BanUserForm(FlaskForm):
    intra_id = StringField(
        "Intra ID<span class=\"text-danger\">*</span>", validators=[
            DataRequired(),
            Regexp(r"^[a-zA-Z-]+$", message="Intra ID supplied contained invalid characters."),
        ]
    )
    photo = FileField("Photo", validators=[FileAllowed(photos)])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    reason = StringField("Reason<span class=\"text-danger\">*</span>", validators=[DataRequired()])
    submit = SubmitField("Add User")

    def validate_intra_id(self, field):
        if BannedUser.query.filter_by(intra_id=field.data, visible=True).first() is not None:
            raise ValidationError(Markup("<strong>%s</strong> is already on the watchlist." % field.data))
