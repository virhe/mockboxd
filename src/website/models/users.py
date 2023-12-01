from flask_login import UserMixin
from ..externals import db


# Class name in plural due to user being reserved
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    watchlist = db.relationship('Watchlist', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}>"
