from app.dto.item import ItemCreate
from app.models import Item
from app.utils import update_model
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def create_item(session: AsyncSession, item_in: ItemCreate, token: dict):
    item = Item(**item_in.model_dump(), owner_id=token["id"])
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def list_item(session: AsyncSession, token: dict, skip: int, limit: int):
    stmt = select(Item).filter(Item.owner_id == token["id"])
    total_result = await session.execute(
        select(func.count()).select_from(stmt.subquery())
    )
    total = total_result.scalar_one()
    result = await session.execute(stmt.offset(skip).limit(limit))
    items = result.scalars().all()
    return items, total


async def get_item(session: AsyncSession, item_id: int, token: dict):
    item = await session.execute(
        select(Item).filter(Item.id == item_id, Item.owner_id == token["id"])
    )
    return item.scalar_one_or_none()


async def update_item(session: AsyncSession, item: Item, item_in: ItemCreate):
    item = update_model(item, item_in)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(session: AsyncSession, item: Item):
    await session.delete(item)
    await session.commit()
    return item


async def change_status(session: AsyncSession, item: Item, status: str):
    item.status = status
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
