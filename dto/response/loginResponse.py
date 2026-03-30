from dataclasses import Field

from pydantic import BaseModel, EmailStr


class LoginResponse(BaseModel):
    user_id: int
    role: str
    access_token: str
    refresh_token: str
    username: str
