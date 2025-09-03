from sqlalchemy.orm import Session
from app.models.user import User
from app.dto import UserCreate


def find_by_username(session: Session, username: str):
    user = session.query(User).filter(User.username == username).first()
    return user


def create_user(session: Session, user_in: UserCreate):
    user = User(**user_in.model_dump())
    session.add(user)
    session.commit()
    return user
