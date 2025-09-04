from typing import Annotated, TypeVar, Type
from fastapi import Depends, Request, HTTPException, Path
from app.db import get_session
from sqlalchemy.orm import Session
from app.services import decode_token
from app.models import Base
from app.services import get_item

SessionDep = Annotated[Session, Depends(get_session)]


def get_token(session: SessionDep, request: Request):
    token = request.headers.get("Authorization", "").split(" ")[-1]
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return decode_token(session, token)


Token = Annotated[str, Depends(get_token)]

T = TypeVar("T", bound=Base)


def get_entity(model: Type[T], id_name: str = "item_id"):
    def dependency(
        entity_id: int = Path(..., alias=id_name),
        db: Session = Depends(get_session),
        current_user: dict = Depends(get_token),
    ) -> T:
        instance = get_item(db, entity_id, current_user)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return instance

    return dependency
