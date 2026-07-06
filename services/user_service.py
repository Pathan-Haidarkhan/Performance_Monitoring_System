from dto.response.managerResponse import ManagerResponseDto
from dto.response.roleResponse import RoleResponse
from dto.response.paginationResponse import PaginatedResponseDto
from models import User
from dto.response.userResponse import UserResponse
from dto.request.registerRequest import RegisterRequest
from extensions import db
from sqlalchemy import or_
from math import ceil

from models.role import Role


class UserService:

    @staticmethod
    def getAllUser(pagesize, page, roleid, isactive, search, sortcolumn, sortdirection):

        query = User.query
        
        if search:
             query = query.filter(
                    or_(User.firstName.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"))
                )
        if roleid:
            query = query.filter(User.roleId == roleid)
        
        if isactive:
            query = query.filter(User.isActive ==(isactive == 'true'))
        

        sortMapping = {
            "name": User.firstName,
            "email": User.email,
            "roleId": User.roleId,
            "isActive": User.isActive
        }

        selectedColumn = sortMapping.get(sortcolumn,User.firstName)

        if sortdirection.lower() == "desc":
            query = query.order_by(selectedColumn.desc())
        else:
            query = query.order_by(selectedColumn.asc())
        
        totalRecords = query.count()
        users = query.offset((page - 1) * pagesize).limit(pagesize).all()


             

        items = [ UserResponse.model_validate(user).model_dump() for user in users]
        userList = PaginatedResponseDto(
            items=items,
            page=page,
            pageSize=pagesize,
            totalRecords=totalRecords,
            totalPages=ceil(totalRecords / pagesize)
        )
        return userList.model_dump(),'Get All user successfully'
    
        # return userList, 'Get All user successfully'


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
            return {'message': 'User not found'}, False, 404
        
        if dto.managerId is not None and user.id == dto.managerId:
            return {"message": "A user cannot be their own manager."}, False, 400
        
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
    
    @staticmethod
    def getUserRoles():

        roles = Role.query.order_by(Role.roleName).all()

        response = [RoleResponse(
            id = role.id,
            name = role.roleName
            ).model_dump() for role in roles]
        
        return response ,True, 200,'Get User Roles successfully'
    
    @staticmethod
    def getManager():

        managers = (
            User.query
            .join(Role)
            .filter(Role.roleName == "manager")
            .order_by(User.firstName)
            .all()
        )

        response = [
            ManagerResponseDto(
                id=user.id,
                name=f"{user.firstName} {user.lastName}"
            ).model_dump()
            for user in managers
        ]

        return response, True, 200, "Users fetched successfully"