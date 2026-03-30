from extensions import db
from datetime import datetime

class PerformanceCalculations(db.Model):
    
    __tablename__ = "PerformanceCalculations"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer,db.ForeignKey('UserMaster.id'), nullable=False)
    metricId = db.Column(db.Integer,db.ForeignKey('PerformanceMaster.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    calculatedScore = db.Column(db.Numeric(6, 2))
    calculatedDate = db.Column(db.DateTime, default=datetime.now)