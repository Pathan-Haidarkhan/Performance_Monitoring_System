from models import Role
from models import User
from utils.handlers import AppException
from extensions import db
from utils.security import generate_token, generate_refresh_token
from dto.response.loginResponse import LoginResponse


class AuthService:


    @staticmethod
    def registration(dto):

        existing_user = User.query.filter_by(email=dto.email).first()
        if existing_user:
            raise AppException(
                    message='Email already registered',
                    status_code=400,
            )
        user = User(
            firstName = dto.firstName,
            lastName = dto.lastName,
            email = dto.email,
            password = dto.password,
            roleId =dto.roleId,
            # roleId = Role.query.filter_by(roleName=dto.get('role')).first(),
            managerId = dto.managerId,
            isActive = dto.isActive
        )
        db.session.add(user)
        db.session.commit()

        return {'message': 'User is created'}, True, 200


    @staticmethod
    def login(dto):

        user = User.query.filter_by(email=dto.email).first()
        if not user or not user.password == dto.password:
            raise AppException(
                message='Invalid credentials',
                status_code=400,
            )
        token = generate_token(user.id,{'role':user.role.roleName})
        refresh = generate_refresh_token(user.id, {'role':user.role.roleName})

        return LoginResponse(
            user_id= user.id,
            role= user.role.roleName,
            access_token= token,
            refresh_token= refresh,
            username= user.firstName + ' ' + user.lastName,
        )