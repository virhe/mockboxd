from ..db import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __repr__(self):
        return f"<Movie {self.name}"
