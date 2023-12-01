from sqlalchemy import func
from ..externals import db


class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user = db.relationship("Users", back_populates="watchlist")
    movie = db.relationship("Movie", back_populates="seen_by")

    def __repr__(self):
        return f"<Watchlist {self.user} - {self.movie}"