
from flask import Flask, render_template, request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required

from dto.request.registerRequest import RegisterRequest
from services.auth_service import AuthService
from utils.apiResponse import api_response
from utils.security import generate_refresh_token, generate_token
from dto.request.loginRequest import LoginRequest

auth_routes = Blueprint( 'auth_routes', __name__,url_prefix='/api/auth')

@auth_routes.route('/login', methods=['POST'])
def login():

        dto = LoginRequest(**request.json)
        responseDto = AuthService.login(dto)
        return api_response(
            success=True,
            message="Login successful",
            data=responseDto.model_dump()
        )

@auth_routes.route('/registration', methods=['POST'])
def registration():

    dto = RegisterRequest(**request.json)

    response, success, status = AuthService.registration(dto)
    return api_response(
        success=success,
        message=response['message'],
        status_code=status
    )



@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    claims = get_jwt()
    new_access = generate_token(
        user_id,
        {"role": claims['role']}
    )

    return api_response(
        success=True,
        message="successfully created access token",
        data={'new_access': new_access},
        status_code=200
    )
