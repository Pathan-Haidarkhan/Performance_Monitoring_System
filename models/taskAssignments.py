from extensions import db
from datetime import datetime

class TaskAssignments(db.Model):

    __tablename__ = 'TaskAssignments'

    id = db.Column(db.Integer, primary_key=True)
    taskId = db.Column(db.Integer, db.ForeignKey('TaskMaster.id'), nullable=False)
    assignedTo = db.Column(db.Integer, db.ForeignKey('UserMaster.id'), nullable=False)
    assignedBy = db.Column(db.Integer, db.ForeignKey('UserMaster.id'), nullable=False)
    statusId = db.Column(db.Integer, db.ForeignKey('TaskStatusMaster.id'), nullable=False)
    dueDate = db.Column(db.Date)
    assignedDate = db.Column(db.DateTime, default=datetime.now)
    progressPercent = db.Column(db.Integer)
    completedDate = db.Column(db.DateTime, nullable=True)