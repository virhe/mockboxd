"""Module implements FlaskForm for adding a movie"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class AddMovieForm(FlaskForm):
    """Form used for adding a movie"""

    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    year = IntegerField("Year")
    submit = SubmitField("Add movie")
