from extensions import db
from datetime import datetime

class TaskActivityLogs(db.Model):

    __tablename__ = 'TaskActivityLogs'

    id = db.Column(db.Integer, primary_key=True)
    assignmentId = db.Column(db.Integer,  db.ForeignKey('TaskAssignments.id'), nullable=False)
    progressPercent = db.Column(db.Integer)
    remarks = db.Column(db.String(255))
    updatedBy = db.Column(db.Integer, db.ForeignKey('UserMaster.id') ,nullable=False)
    updatedDate = db.Column(db.DateTime, default=datetime.now)