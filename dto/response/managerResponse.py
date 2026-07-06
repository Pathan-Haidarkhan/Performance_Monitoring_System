from pydantic import BaseModel

class ManagerResponseDto(BaseModel):
    id: int
    name: str