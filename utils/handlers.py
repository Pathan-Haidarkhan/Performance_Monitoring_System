from werkzeug.exceptions import HTTPException
from extensions import jwt
from utils.apiResponse import api_response
from extensions import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class AppException(Exception):
    def __init__(self, message, status_code, error=None):
        self.message = message
        self.status_code = status_code
        self.error = error
        super().__init__(self.message)


def register_error_handlers(app):

    @app.errorhandler(AppException)
    def handle_error(e):
        return api_response(
            success=False,
            message=e.message,
            error=e.error,
            status_code=e.status_code
        )


    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return api_response(
            success=False,
            message=e.name,
            error=e.description,
            status_code=e.code
        )



    @app.errorhandler(Exception)
    def handle_general_exception(e):
        return api_response(
            success=False,
            message="Internal Server Error",
            error=str(e),
            status_code=500
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_db_exception(e):
        db.session.rollback()
        return api_response(
            success=False,
            message="Database Error",
            error=str(e),
            status_code=500
        )


def register_jwt_handlers(app):

    @jwt.unauthorized_loader
    def handle_unauthorized(e):
        return api_response(
            success=False,
            message="Unauthorized",
            error=str(e),
            status_code=401
        )


    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        return api_response(
            success=False,
            message="Expired token",
            status_code=401
        )


    @jwt.invalid_token_loader
    def handle_invalid_token(e):
        return api_response(
            success=False,
            message="Invalid token",
            error=str(e),
        )