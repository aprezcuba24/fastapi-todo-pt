from typing import Annotated
from fastapi import Depends
from app.db import get_session
from sqlalchemy.orm import Session

SessionDep = Annotated[Session, Depends(get_session)]
