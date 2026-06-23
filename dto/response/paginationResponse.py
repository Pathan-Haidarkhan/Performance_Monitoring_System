from pydantic import BaseModel
from typing import Generic, List, TypeVar

T = TypeVar("T")


class PaginatedResponseDto(BaseModel, Generic[T]):
    items: List[T]
    page: int
    pageSize: int
    totalRecords: int
    totalPages: int