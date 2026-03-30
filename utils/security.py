from functools import wraps
from flask_jwt_extended import create_access_token, get_jwt, create_refresh_token, verify_jwt_in_request, \
    get_jwt_identity

from models import User
from utils.handlers import AppException


def generate_token(user_id, claims) -> str:
    return create_access_token(
        identity=str(user_id),
        additional_claims=claims
    )


def generate_refresh_token(user_id,claims) -> str:
     return create_refresh_token(
        identity=str(user_id),
         additional_claims=claims
     )

def current_user():
    userId = get_jwt_identity()
    return userId

def current_user_role():
    identity = get_jwt()
    return identity.get('role')

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            claims = get_jwt().get('role')

            if claims.lower() not in [role.lower() for role in roles]:
                raise AppException(
                    message='Access denied, Do not have permission to access this resource',
                    status_code=403
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
