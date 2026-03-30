from extensions import db
from datetime import datetime

class TaskMaster(db.Model):

    __tablename__ = 'TaskMaster'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.Enum('LOW', 'MEDIUM', 'HIGH'), default='MEDIUM')
    createdBy = db.Column(db.Integer, db.ForeignKey('UserMaster.id'), nullable=False)
    createdDate = db.Column(db.DateTime, default=datetime.now)
    updatedDate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)