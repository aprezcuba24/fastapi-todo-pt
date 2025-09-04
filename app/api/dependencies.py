from typing import Annotated, TypeVar, Type
from fastapi import Depends, Request, HTTPException, Path
from app.db import get_session
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.user import get_user_by_token
from app.models import Base
from app.services import get_item

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(session: SessionDep, request: Request):
    token = request.headers.get("Authorization", "").split(" ")[-1]
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return get_user_by_token(session, token)


CurrentUser = Annotated[User, Depends(get_current_user)]

T = TypeVar("T", bound=Base)


def get_entity(model: Type[T], id_name: str = "item_id"):
    def dependency(
        entity_id: int = Path(..., alias=id_name),
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user),
    ) -> T:
        instance = get_item(db, current_user, entity_id)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return instance

    return dependency
