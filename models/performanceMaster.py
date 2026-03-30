from extensions import db
from datetime import datetime

class PerformanceMaster(db.Model):
    
    __tablename__ = "PerformanceMaster"

    id = db.Column(db.Integer, primary_key=True)
    metricName = db.Column(db.String(100), nullable=False, unique=True)
    metricWeight = db.Column(db.Numeric(5, 2), nullable=False)
    description = db.Column(db.String(255))
    isActive = db.Column(db.Boolean, default=True)
    createdDate = db.Column(db.DateTime, default=datetime.now)