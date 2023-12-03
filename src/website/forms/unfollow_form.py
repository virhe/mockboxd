"""Module implements FlaskForm for unfollowing a user"""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class UnfollowForm(FlaskForm):
    """Form used for unfollowing a user"""

    submit = SubmitField("Unfollow")
