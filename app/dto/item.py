from pydantic import BaseModel, field_validator
from typing import List
from app.models import StatusEnum
from datetime import datetime


class ItemCreate(BaseModel):
    title: str
    description: str


class ItemResponse(ItemCreate):
    id: int
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


class ListResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    skip: int
    limit: int


class StatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    def validate_status(cls, v):
        try:
            return StatusEnum(v).value
        except ValueError:
            raise ValueError(f"Status must be one of: {[e.value for e in StatusEnum]}")
