from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    description: str
