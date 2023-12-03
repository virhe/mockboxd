"""Module implements movie class for ORM"""

from sqlalchemy import func
from ..externals import db


class Movie(db.Model):
    """Represents a movie"""

    # pylint: disable=not-callable

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ratings = db.relationship("Rating", back_populates="movie")
    comments = db.relationship("Comment", back_populates="movie")
    seen_by = db.relationship("Watchlist", back_populates="movie")

    def __repr__(self):
        return f"<Movie {self.name}"
