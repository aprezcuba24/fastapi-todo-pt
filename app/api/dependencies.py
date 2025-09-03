from typing import Annotated
from fastapi import Depends, Request, HTTPException
from app.db import get_session
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.user import get_user_by_token

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(session: SessionDep, request: Request):
    token = request.headers.get("Authorization", "").split(" ")[-1]
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return get_user_by_token(session, token)


CurrentUser = Annotated[User, Depends(get_current_user)]
