from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class TaskRequest(BaseModel):

    title : str = Field(..., min_length=5, max_length=255)
    description : str = Field( max_length=255)
    priority : str


class TaskAssignmentRequestDTO(BaseModel):

    taskId: int = Field(..., gt=0)
    assignedTo: int = Field(..., gt=0)
    statusId : int = Field(..., gt=0)
    dueDate: date = Field(..., description="Task due date (YYYY-MM-DD)")
    remarks: Optional[str] = Field(None, max_length=500)



class TaskProgressUpdateRequestDTO(BaseModel):

    assignmentId: int = Field(..., gt=0)
    statusId: int = Field( ..., gt=0)
    matricId: int = Field(..., gt=0)
    progressPercent: int = Field(...,ge=0,le=100)
    remarks: Optional[str] = Field(None,max_length=500)



class TaskReassignRequestDTO(BaseModel):
    assignmentId: int
    newUserId: int
    progressPercent: int = Field(..., ge=0, le=100)
    remarks: Optional[str] = Field(None, max_length=500)

    class Config:
        from_attributes = True
       

    def to_dict(self):
        return self.model_dump(exclude_none=True)


class StatusRequestModel(BaseModel):
    statusName: str = Field(..., min_length=5, max_length=30)
    isFinal: bool = Field(default=False)

