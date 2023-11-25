from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchMovieForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField("Search")
