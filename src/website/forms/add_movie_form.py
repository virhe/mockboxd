"""Module implements FlaskForm for adding a movie"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class AddMovieForm(FlaskForm):
    """Form used for adding a movie"""

    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    year = IntegerField("Year")
    description = TextAreaField("Description", validators=[DataRequired()])

    genres = [
        "Adventure",
        "Action",
        "Drama",
        "Comedy",
        "Thriller",
        "Horror",
        "Romantic",
        "Musical",
        "Documentary",
    ]
    genre = SelectField("Genre", choices=genres, validators=[DataRequired()])

    submit = SubmitField("Add movie")
