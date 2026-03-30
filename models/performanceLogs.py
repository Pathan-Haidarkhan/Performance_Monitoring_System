from extensions import db
from datetime import datetime

class PerformanceLogs(db.Model):
    
    __tablename__ = "PerformanceLogs"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer,db.ForeignKey('UserMaster.id'), nullable=False)
    assignmentId = db.Column(db.Integer,db.ForeignKey('TaskAssignments.id'), nullable=False)
    metricId = db.Column(db.Integer,db.ForeignKey('PerformanceMaster.id'), nullable=False)
    metricValue = db.Column(db.Numeric(5, 2), nullable=False)
    logDate = db.Column(db.Date, nullable=False)
    createdDate = db.Column(db.DateTime, default=datetime.now)