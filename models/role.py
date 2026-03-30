from extensions import db
from datetime import datetime


class Role(db.Model):

    __tablename__ = 'RoleMaster'

    id = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(50), nullable=False)
    createdDate = db.Column(db.DateTime, default=datetime.now)
    updatedDate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship(
        "User",
        back_populates ="role" )