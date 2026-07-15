from pydantic import BaseModel
from typing import TypeVar, Generic,List

T = TypeVar("T")
class DepartmentResponse(BaseModel):
    
    DepartmentId: int
    DepartmentName: str
    Description: str
    ManagerName: str
    isActive : bool 


    class Config:
        from_attributes = True


class DepartmentMainResponse(BaseModel, Generic[T]):
     items: List[T]
     totalRecords: int