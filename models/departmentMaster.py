from extensions import db


class DepartmentMaster(db.Model) :
    
    __tablename__ = "DepartmentMaster"

    DepartmentId = db.Column(db.Integer, primary_key = True)
    DepartmentName = db.Column(db.String(150), nullable=False)
    Description = db.Column(db.Text)
    ManagerId = db.Column(db.Integer,db.ForeignKey('UserMaster.id'), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
