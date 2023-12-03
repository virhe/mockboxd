"""Module implements FlaskForm for following a user"""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class FollowForm(FlaskForm):
    """Form used for following a user"""

    submit = SubmitField("Follow")
