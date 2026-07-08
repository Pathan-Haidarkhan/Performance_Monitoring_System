from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    
    DepartmentId: int
    DepartmentName: str
    Description: str
    ManagerId: int
    isActive : bool 


    class Config:
        from_attributes = True