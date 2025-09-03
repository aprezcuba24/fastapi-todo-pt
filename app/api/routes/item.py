from fastapi import APIRouter, Query
from app.api.dependencies import SessionDep, CurrentUser
from app.services import (
    create_item,
    list_item as service_list_item,
    get_item as service_get_item,
    update_item as service_update_item,
    delete_item as service_delete_item,
    change_status as service_change_status,
)
from app.dto import ItemCreate, ListResponse, StatusUpdate, ItemResponse

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


@router.post("/", response_model=ItemResponse)
def register(session: SessionDep, current_user: CurrentUser, item_in: ItemCreate):
    return create_item(session, item_in, current_user)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(session: SessionDep, current_user: CurrentUser, item_id: int):
    return service_get_item(session, current_user, item_id)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    session: SessionDep, current_user: CurrentUser, item_id: int, item_in: ItemCreate
):
    return service_update_item(session, current_user, item_id, item_in)


@router.delete("/{item_id}")
def delete_item(session: SessionDep, current_user: CurrentUser, item_id: int):
    return service_delete_item(session, current_user, item_id)


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item_status(
    session: SessionDep,
    current_user: CurrentUser,
    item_id: int,
    status_update: StatusUpdate,
):
    return service_change_status(session, current_user, item_id, status_update.status)
