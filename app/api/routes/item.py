from fastapi import APIRouter, Query, Depends
from app.api.dependencies import SessionDep, CurrentUser, get_entity
from app.services import (
    create_item,
    list_item as service_list_item,
    get_item as service_get_item,
    update_item as service_update_item,
    delete_item as service_delete_item,
    change_status as service_change_status,
)
from app.dto import ItemCreate, ListResponse, StatusUpdate, ItemResponse
from app.models import Item

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
def get_item(
    session: SessionDep,
    current_user: CurrentUser,
    item: Item = Depends(get_entity(Item)),
):
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    session: SessionDep,
    current_user: CurrentUser,
    item_in: ItemCreate,
    item: Item = Depends(get_entity(Item)),
):
    return service_update_item(session, current_user, item, item_in)


@router.delete("/{item_id}")
def delete_item(
    session: SessionDep,
    current_user: CurrentUser,
    item: Item = Depends(get_entity(Item)),
):
    return service_delete_item(session, current_user, item)


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item_status(
    session: SessionDep,
    current_user: CurrentUser,
    status_update: StatusUpdate,
    item: Item = Depends(get_entity(Item)),
):
    return service_change_status(session, current_user, item, status_update.status)
