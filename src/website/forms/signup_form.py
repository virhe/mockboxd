"""Module implements FlaskForm for signing up"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class SignupForm(FlaskForm):
    """Form used for signing up"""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=30)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=4, max=255)]
    )
    submit = SubmitField("Sign up")
