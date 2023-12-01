"""Module implements FlaskForm for rating a movie"""

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class RatingForm(FlaskForm):
    """Form used for rating a movie"""

    rating = RadioField(
        "Rating",
        choices=[("5", "5"), ("4", "4"), ("3", "3"), ("2", "2"), ("1", "1")],
        validators=[DataRequired()],
    )

    submit = SubmitField("Submit")
