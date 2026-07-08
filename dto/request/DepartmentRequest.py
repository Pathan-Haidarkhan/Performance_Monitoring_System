from pydantic import BaseModel, Field

class DepartmentRequest(BaseModel) :

    DepartmentName: str = Field(..., min_length=3, max_length=150)
    Description: str
    ManagerId: int
    isActive: bool = True 
