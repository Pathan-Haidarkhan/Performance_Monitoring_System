from extensions import db
from datetime import datetime

class PerformanceSummary(db.Model):
    
    __tablename__ = "PerformanceSummary"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer,db.ForeignKey('UserMaster.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    totalScore = db.Column(db.Numeric(6, 2))
    rating = db.Column(db.String(20))
    generatedDate = db.Column(db.DateTime, default=datetime.now)
