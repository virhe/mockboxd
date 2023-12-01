"""Module implements FlaskForm for commenting"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    """Form used for adding a comment"""

    comment = TextAreaField(
        "Comment", validators=[DataRequired(), Length(min=4, max=255)]
    )

    submit = SubmitField("Post")
