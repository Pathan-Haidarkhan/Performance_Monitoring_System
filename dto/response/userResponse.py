from pydantic import BaseModel, computed_field


class UserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    password: str
    roleId: int
    managerId: int | None = None
    isActive: bool

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    class Config:
        from_attributes = True