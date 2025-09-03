from fastapi import APIRouter
from app.api.dependencies import SessionDep, CurrentUser

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def register(session: SessionDep, current_user: CurrentUser):
    return current_user
