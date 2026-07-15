from flask import Blueprint, request
from flask_jwt_extended import  jwt_required
from services.department_service import DepartmentService
from utils.apiResponse import api_response
from utils.security import role_required

from dto.request.DepartmentRequest import DepartmentRequest


department_routes = Blueprint('department_routes', __name__,url_prefix='/api/department')


@department_routes.route('/createDepartment', methods=['POST'])
@jwt_required()  
@role_required('ADMIN')
def CreateDepartment():

    dto = DepartmentRequest( **request.json)
    response, success, status = DepartmentService.createDepartment(dto)
    return api_response(
        success=success,
        data=response['departmentId'],
        message=response['message'],
        status_code=status
    )

@department_routes.route('/getDepartmentById/<int:deptId>', methods=['GET'])
@jwt_required()  
@role_required('ADMIN')
def getDepartmentById(deptId: int):

    responseDto = DepartmentService.getDepartmentById(deptId)
    return api_response(
        success=True,
        data=responseDto,
        status_code=200
    )


@department_routes.route('/getAllDepartments', methods=['GET'])
@jwt_required()  
@role_required('ADMIN')
def getAllDepartments():

    Search = request.args.get("search", type=str)
    isActive = request.args.get("isactive", type=str)

    responseDto = DepartmentService.getAllDepartments(search=Search, isactive=isActive)
    return api_response(
        success=True,
        data=responseDto,
        status_code=200
    )



@department_routes.route('/updateDepartmentById/<int:deptId>', methods=['PUT'])
@jwt_required()  
@role_required('ADMIN')
def updateDepartmentById(deptId: int):
    
    dto = DepartmentRequest(**request.json)
    response,success, status = DepartmentService.updateDepartmentById(dto, deptId)
    return api_response(
        status_code=status,
        data=response['departmentId'],
        message= response['message'],
        success=success
    )

@department_routes.route('/deleteDepartmentById/<int:deptId>', methods=['DELETE'])
@jwt_required()  
@role_required('ADMIN')
def deleteDepartmentById(deptId: int):
    
    response,success, status = DepartmentService.deleteDepartmentById(deptId)
    return api_response(
        status_code=status,
        data=response['departmentId'],
        message= response['message'],
        success=success
    )
