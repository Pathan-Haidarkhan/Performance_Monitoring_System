from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    firstName: str = Field(...,min_length=2, max_length=50)
    lastName: str = Field(...,min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(...,min_length=6)
    roleId: int
    managerId: int | None = None
    isActive: bool = True