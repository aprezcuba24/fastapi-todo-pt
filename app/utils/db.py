from app.models.base import Base
from pydantic import BaseModel


def update_model(model: Base, schema: BaseModel):
    update_data = schema.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(model, key, value)
    return model
