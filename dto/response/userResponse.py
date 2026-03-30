from pydantic import BaseModel


class UserResponse(BaseModel):
    firstName: str
    lastName: str
    email: str
    roleId: int
    managerId: int | None = None
    isActive: bool

    class Config:
        from_attributes = True