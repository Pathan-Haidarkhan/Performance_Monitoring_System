from pydantic import BaseModel, Field
from datetime import date
from typing import List


class TaskResponseDTO(BaseModel):
    title: str
    priority: str
    assignedTo: int
    status: str

    class Config:
        from_attributes  = True


class TaskListItemResponseDTO(BaseModel):
    taskId: int = Field(..., gt=0)
    title: str
    status: str
    priority: str
    dueDate: date

    class Config:
        from_attributes = True

    def to_dict(self):
        return self.model_dump(exclude_none=True)


class TaskListResponseDTO(BaseModel):

    tasks: List[TaskListItemResponseDTO]

    class Config:
        from_attributes = True

    def to_dict(self):
        return self.model_dump(exclude_none=True)


class TaskStatusHistoryItemResponseDTO(BaseModel):
    status: str
    progress: int
    updatedDate: date

    class Config:
        from_attributes = True

    def to_dict(self):
        return self.model_dump(exclude_none=True)



class TaskStatusHistoryResponseDTO(BaseModel):
    history: List[TaskStatusHistoryItemResponseDTO]

    class Config:
        from_attributes = True

    def to_dict(self):
        return self.model_dump(exclude_none=True)

class TaskStatusResponseDTO(BaseModel):
    id: int
    status: str
    updatedDate: date

    class Config:
        from_attributes = True

    def to_dict(self):
        return self.model_dump(exclude_none=True)