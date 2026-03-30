from models import User
from dto.response.userResponse import UserResponse
from dto.request.registerRequest import RegisterRequest
from extensions import db


class UserService:

    @staticmethod
    def getAllUser():

        users = User.query.all()
        userList = [ UserResponse.from_orm(user).model_dump() for user in users]
        return userList


    @staticmethod
    def getUserById(id:int):

        user = User.query.get(id)
        if user is None:
            return {'message': 'User not found'}, False, 400

        return UserResponse.from_orm(user).model_dump()


    @staticmethod
    def updateUserById(dto: RegisterRequest, id:int):

        user = User.query.get(id)
        if user is None:
            return {'message': 'User not found'}, False, 400

        updatedData = dto.model_dump(exclude_none=True)

        for key, value in updatedData.items():
            setattr(user, key, value)
        db.session.commit()

        return {'message': 'User updated successfully'}, True, 200

    @staticmethod
    def deleteUserById(id: int):
        user = User.query.get(id)
        if user is None:
            return {'message': 'User not found'}, False, 400
        db.session.delete(user)
        db.session.commit()
        return {'userId': id}, True, 200,'User deleted successfully'