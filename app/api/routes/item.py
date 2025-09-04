from fastapi import APIRouter, Query, Depends
from app.api.dependencies import SessionDep, Token, get_entity
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


@router.get("", response_model=ListResponse)
async def list_item(
    session: SessionDep,
    token: Token,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    items, total = await service_list_item(session, token, skip, limit)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("", response_model=ItemResponse)
async def register(session: SessionDep, token: Token, item_in: ItemCreate):
    return await create_item(session, item_in, token)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    session: SessionDep,
    item: Item = Depends(get_entity(Item)),
):
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    session: SessionDep,
    item_in: ItemCreate,
    item: Item = Depends(get_entity(Item)),
):
    return await service_update_item(session, item, item_in)


@router.delete("/{item_id}")
async def delete_item(
    session: SessionDep,
    item: Item = Depends(get_entity(Item)),
):
    return await service_delete_item(session, item)


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item_status(
    session: SessionDep,
    status_update: StatusUpdate,
    item: Item = Depends(get_entity(Item)),
):
    return await service_change_status(session, item, status_update.status)
