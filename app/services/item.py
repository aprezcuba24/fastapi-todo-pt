from sqlalchemy.orm import Session
from app.dto.item import ItemCreate
from app.models import Item, User


def create_item(session: Session, item: ItemCreate, owner: User):
    item = Item(**item.model_dump(), owner_id=owner.id)
    session.add(item)
    session.commit()
    return item


def list_item(session: Session, owner: User, skip: int, limit: int):
    query = session.query(Item).filter(Item.owner_id == owner.id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total
