from sqlalchemy import func
from ..externals import db


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    movie = db.relationship("Movie", back_populates="ratings")

    def __repr__(self):
        return f"<Rating - {self.user_id} - {self.movie_id}>"
