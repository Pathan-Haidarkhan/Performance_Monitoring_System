from pydantic import BaseModel
from typing import Optional
from datetime import date

class PerformanceMetricResponseDTO(BaseModel):
    id : int
    metricName: str
    metricWeight: float
    description: Optional[str]
    isActive: bool
    createdDate: date


    class Config:
        from_attributes  = True


class PerformanceCalculationDTO(BaseModel):
    id : int
    userId : int
    metricId : int
    month: int
    year: int
    calculatedScore: float
    calculatedDate: date


    class Config:
        from_attributes  = True


class PerformanceSummaryDTO(BaseModel):
    id : int
    userId : int

    month: int
    year: int
    totalScore: float
    rating: str
    generatedDate: date

    class Config:
        from_attributes  = True


class CompanyRankingItemDTO(BaseModel):
    rank: int
    employee: str
    score: float
    rating: str