from typing import Optional

from pydantic import BaseModel, EmailStr,Field


class UpdateUserRequestDTO(BaseModel):
    firstName: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = None

    class Config:
        from_attributes = True