from pydantic import BaseModel
from typing import List


class ItemResponse(BaseModel):
    title: str
    description: str


class ItemCreate(ItemResponse):
    pass


class ListResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    skip: int
    limit: int
