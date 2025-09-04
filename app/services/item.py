from sqlalchemy.orm import Session
from app.dto.item import ItemCreate
from app.models import Item
from app.utils import update_model


def create_item(session: Session, item_in: ItemCreate, token: dict):
    item = Item(**item_in.model_dump(), owner_id=token["id"])
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def list_item(session: Session, token: dict, skip: int, limit: int):
    query = session.query(Item).filter(Item.owner_id == token["id"])
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_item(session: Session, item_id: int, token: dict):
    item = (
        session.query(Item)
        .filter(Item.id == item_id, Item.owner_id == token["id"])
        .first()
    )
    return item


def update_item(session: Session, item: Item, item_in: ItemCreate):
    item = update_model(item, item_in)
    session.add(item)
    session.commit()
    return item


def delete_item(session: Session, item: Item):
    session.delete(item)
    session.commit()
    return item


def change_status(session: Session, item: Item, status: str):
    item.status = status
    session.add(item)
    session.commit()
    return item
