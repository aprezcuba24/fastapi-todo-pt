from fastapi import APIRouter, Query
from app.api.dependencies import SessionDep, CurrentUser
from app.services import create_item, list_item as service_list_item
from app.dto import ItemCreate, ListResponse

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ListResponse)
def list_item(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    items, total = service_list_item(session, current_user, skip, limit)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/")
def register(session: SessionDep, current_user: CurrentUser, item_in: ItemCreate):
    return create_item(session, item_in, current_user)
