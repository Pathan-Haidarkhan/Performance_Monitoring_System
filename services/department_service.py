from dto.request.DepartmentRequest import DepartmentRequest
from dto.response.departmentResponse import DepartmentResponse
from extensions import db
from models import DepartmentMaster
from utils.security import current_user, current_user_role


class DepartmentService:

    @staticmethod
    def createDepartment(dto: DepartmentRequest):

        department = DepartmentMaster(
            DepartmentName = dto.DepartmentName,
            Description = dto.Description,
            ManagerId = dto.ManagerId,
            isActive = dto.isActive
        )

        db.session.add(department)
        db.session.commit()
        return {'departmentId': department.DepartmentId, 'message':'Department Created successfully'}, True, 200
    
    @staticmethod
    def getDepartmentById(deptId: int):

        detail = DepartmentMaster.query.get(deptId)

        if detail is None:
              return {'message': 'Department not found'}, False, 404
        
        return DepartmentResponse.from_orm(detail).model_dump()
    
    @staticmethod
    def updateDepartmentById(dto: DepartmentRequest, deptId: int):
        
        department = DepartmentMaster.query.get(deptId)
        if department is None:
            return {'message': 'Department not found'}, False, 404
        
        updatedData = dto.model_dump(exclude_none=True)

        for key, value in updatedData.items():
            setattr(department,key,value)
        db.session.commit()

        return {'departmentId': department.DepartmentId ,'message': 'Department updated successfully'}, True, 200
    
    @staticmethod
    def deleteDepartmentById(deptId: int):

        department = DepartmentMaster.query.get(deptId)
        
        if department is None:
            return {'message': 'Department not found'}, False, 404
       
        db.session.delete(department)
        db.session.commit()
        return {'departmentId': department.DepartmentId, 'message': 'Department deleted successfully'}, True, 200,
