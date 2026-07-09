from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import Priority, Status


class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1)
    priority: Priority
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    status: Status


class ItemResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: str
    title: str
    priority: Priority
    status: Status
    created_at: datetime = Field(serialization_alias="createdAt")
    description: Optional[str] = None


class PaginatedItems(BaseModel):
    items: list[ItemResponse]
    page: int
    limit: int
    total: int
