from pydantic import BaseModel, Field
from typing import Optional

class PerformanceMetricCreateDTO(BaseModel):
    metricName: str = Field(..., min_length=3, max_length=100)
    metricWeight: float = Field(..., gt=0, le=100)
    description: Optional[str] = Field(None, max_length=255)


class PerformanceMetricUpdateDTO(BaseModel):
    metricName: str = Field(..., min_length=3, max_length=100)
    metricWeight: float = Field(None, gt=0, le=100)
    description: Optional[str] = Field(None, max_length=255)
    isActive: Optional[bool]
