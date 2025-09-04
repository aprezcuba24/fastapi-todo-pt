import jwt
import bcrypt
from sqlalchemy.orm import Session, load_only
from app.models.user import User
from app.dto import UserCreate, UserLogin
from app.config import settings


def find_by_username(session: Session, username: str):
    user = session.query(User).filter(User.username == username).first()
    return user


def create_user(session: Session, user_in: UserCreate):
    password = hash_password(user_in.password)
    data = user_in.model_dump(exclude={"password"})
    user = User(**data, password=password)
    session.add(user)
    session.commit()
    return user


def get_token(session: Session, user_in: UserLogin):
    user = (
        session.query(User)
        .options(load_only(User.id, User.username, User.name))
        .filter(User.username == user_in.username)
        .first()
    )
    password = hash_password(user_in.password)
    if not user or not bcrypt.checkpw(user_in.password.encode("utf-8"), password):
        return None
    payload = {
        "id": user.id,
        "username": user.username,
        "name": user.name,
    }
    token = jwt.encode(payload, settings.SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_token(session: Session, token: str):
    return jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALGORITHM])


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
