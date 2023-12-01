from sqlalchemy import func
from ..externals import db


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    follower = db.relationship("Users", foreign_keys=[follower_id], back_populates="followed")
    followed = db.relationship("Users", foreign_keys=[followed_id], back_populates="followers")

    def __repr__(self):
        return f"<Follower - {self.follower_id} - {self.followed_id}>"
