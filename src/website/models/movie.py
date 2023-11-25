from sqlalchemy import func
from ..externals import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ratings = db.relationship("Rating", back_populates="movie")
    comments = db.relationship("Comment", back_populates="movie")

    def __repr__(self):
        return f"<Movie {self.name}"
