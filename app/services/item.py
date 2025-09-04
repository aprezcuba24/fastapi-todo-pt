from sqlalchemy.orm import Session
from app.dto.item import ItemCreate
from app.models import Item, User
from app.utils import update_model


def create_item(session: Session, item_in: ItemCreate, owner: User):
    item = Item(**item_in.model_dump(), owner_id=owner.id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def list_item(session: Session, owner: User, skip: int, limit: int):
    query = session.query(Item).filter(Item.owner_id == owner.id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total


def get_item(session: Session, owner: User, item_id: int):
    item = (
        session.query(Item)
        .filter(Item.id == item_id, Item.owner_id == owner.id)
        .first()
    )
    return item


def update_item(session: Session, owner: User, item: Item, item_in: ItemCreate):
    item = update_model(item, item_in)
    session.add(item)
    session.commit()
    return item


def delete_item(session: Session, owner: User, item: Item):
    session.delete(item)
    session.commit()
    return item


def change_status(session: Session, owner: User, item: Item, status: str):
    item.status = status
    session.add(item)
    session.commit()
    return item
