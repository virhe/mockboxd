"""Module implements FlaskForm for searching for a movie by name"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class SearchMovieForm(FlaskForm):
    """Form used for searching for a movie by name"""

    name = StringField("Name", validators=[Length(max=255)])
    submit = SubmitField("Search")
