
from datetime import datetime
from extensions import db

class User(db.Model):

    __tablename__ = 'UserMaster'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50) , nullable=False)
    lastName = db.Column(db.String(50) , nullable=False)
    email = db.Column(db.String(200) , nullable=False,unique=True)
    password = db.Column(db.String(300) , nullable=False)
    roleId = db.Column(db.Integer , db.ForeignKey("RoleMaster.id"),nullable=False)
    managerId = db.Column(db.Integer , db.ForeignKey("UserMaster.id"),nullable=True)
    isActive = db.Column(db.Boolean, default=True)
    createdDate = db.Column(db.DateTime, default=datetime.now)
    updatedDate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def FullName(self):
        return f"{self.firstName} {self.lastName}"
    
    role  = db.relationship(
        "Role",
        back_populates="user")

    manager = db.relationship(
        "User",
        remote_side=[id],
        backref="subordinates"
    )