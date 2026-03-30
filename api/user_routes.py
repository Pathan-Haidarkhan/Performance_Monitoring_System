from flask import request, jsonify,Blueprint
from flask_jwt_extended import get_jwt, jwt_required

from dto.request.registerRequest import RegisterRequest
from services.auth_service import AuthService
from utils.apiResponse import api_response
from utils.security import role_required
from services.user_service import UserService

user_routes = Blueprint('user_routes', __name__,url_prefix='/api/user')


@user_routes.route('/createUser', methods=['POST'])
@jwt_required()
@role_required('ADMIN')
def createUser():

    dto = RegisterRequest(**request.json)
    response, success, status = AuthService.registration(dto)
    return api_response(
        success=success,
        message=response['message'],
        status_code=status
    )

@user_routes.route('/getAllUser', methods=['GET'])
@jwt_required()
@role_required('ADMIN')
def getAllUser():

    responseDto = UserService.getAllUser()
    return api_response(
        success=True,
        data=responseDto,
        status_code=200
    )

@user_routes.route('/getUserById/<int:userId>', methods=['GET'])
@jwt_required()
@role_required('ADMIN','MANAGER', 'EMPLOYEE')
def getUserById(userId: int):

    responseDto = UserService.getUserById(userId)
    return api_response(
        success=True,
        data=responseDto,
        status_code=200
    )


@user_routes.route('/updateUser/<int:userId>', methods=['PUT'])
@jwt_required()
@role_required('ADMIN','EMPLOYEE')
def updateUser(userId: int):

    requestDto = RegisterRequest(**request.json)
    response, success, status = UserService.updateUserById(requestDto,userId)
    return api_response(
        success=success,
        data=response['message'],
        status_code=status
    )

@user_routes.route('/deleteUser/<int:userId>', methods=['DELETE'])
@jwt_required()
@role_required('ADMIN')
def deleteUser(userId: int):

    response, success, status,message = UserService.deleteUserById(userId)
    return api_response(
        success=success,
        message=message,
        data=response,
        status_code=status
    )