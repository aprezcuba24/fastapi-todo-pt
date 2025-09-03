from fastapi import APIRouter
from app.api.dependencies import SessionDep, CurrentUser
from app.services import create_item, list_item
from app.dto import ItemCreate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def list_item(session: SessionDep, current_user: CurrentUser):
    return list_item(session, current_user)


@router.post("/")
def register(session: SessionDep, current_user: CurrentUser, item_in: ItemCreate):
    return create_item(session, item_in, current_user)
