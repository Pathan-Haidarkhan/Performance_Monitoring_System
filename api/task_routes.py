from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.security import role_required
from dto.request.taskRequest import TaskRequest, TaskAssignmentRequestDTO, TaskReassignRequestDTO ,TaskProgressUpdateRequestDTO, StatusRequestModel
from services.task_service import TaskService
from utils.apiResponse import api_response



task_routes = Blueprint('task_routes', __name__, url_prefix='/api/task')
@task_routes.route('/createTask', methods=['POST'])
@jwt_required()
@role_required('ADMIN','MANAGER')
def createTask():

    taskRequest = TaskRequest(**request.json)
    response, success ,status = TaskService.createTask(taskRequest)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )

@task_routes.route('/updateTask/<int:task_id>', methods=['PUT'])
@jwt_required()
@role_required('ADMIN','MANAGER')
def updateTask(task_id):

    taskRequest = TaskRequest(**request.json)
    response, success, status = TaskService.updateTask(task_id, taskRequest)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/deleteTask/<int:task_id>', methods=['DELETE'])
@jwt_required()
@role_required('ADMIN')
def deleteTask(task_id):

    response, success, status = TaskService.deleteTask(task_id)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/assignTask', methods=['POST'])
@jwt_required()
@role_required('ADMIN','MANAGER')
def assignTask():

    dtoRequest = TaskAssignmentRequestDTO(**request.json)
    response, success, status = TaskService.assignTask(dtoRequest)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )

@task_routes.route('/reAssignTask', methods=['PUT'])
@jwt_required()
@role_required('ADMIN','MANAGER')
def reAssignTask():

    dtoRequest = TaskReassignRequestDTO(**request.json)
    response, success, status = TaskService.reAssignTask(dtoRequest)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/getTask/<int:taskId>', methods=['GET'])
@jwt_required()
@role_required('ADMIN','MANAGER','EMPLOYEE')
def getTask(taskId):

    response, success, status = TaskService.getTask(taskId)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/updateTaskStatus', methods=['POST'])
@jwt_required()
def updateTaskStatus():

    dto = TaskProgressUpdateRequestDTO(**request.json)
    response, success, status = TaskService.updateTaskStatus(dto)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/getAllStatus', methods=['GET'])
@jwt_required()
@role_required('ADMIN','MANAGER')
def getAllStatus():
    response, success, status = TaskService.getAllStatus()
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/createStatus', methods=['POST'])
@jwt_required()
@role_required('ADMIN')
def createStatus():
    dto = StatusRequestModel(**request.json)
    response, success, status = TaskService.createStatus(dto)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/updateStatus/<int:status_id>', methods=['PUT'])
@jwt_required()
@role_required('ADMIN','MANAGER')
def updateStatus(status_id):
    dto = StatusRequestModel(**request.json)
    response, success, status = TaskService.updateStatus(status_id, dto)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )


@task_routes.route('/deleteStatus/<int:status_id>', methods=['DELETE'])
@jwt_required()
@role_required('ADMIN')
def deleteStatus(status_id):
    response, success, status = TaskService.deleteStatus(status_id)
    return api_response(
        success=success,
        message=response['message'],
        data=response,
        status_code=status
    )