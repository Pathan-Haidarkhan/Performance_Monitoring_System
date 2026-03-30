from extensions import db
from datetime import datetime

class TaskStatusMaster(db.Model):

    __tablename__ = 'TaskStatusMaster'
    id = db.Column(db.Integer, primary_key=True)
    statusName = db.Column(db.String(50), nullable=False)
    isFinal = db.Column(db.Boolean, default=False)
    createdDate = db.Column(db.DateTime, default=datetime.now)
    updatedDate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)