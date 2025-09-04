import jwt
import bcrypt
from sqlalchemy.orm import load_only
from app.models.user import User
from app.dto import UserCreate, UserLogin
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def find_by_username(session: AsyncSession, username: str):
    user = await session.execute(
        select(User)
        .options(load_only(User.id, User.username, User.name))
        .filter(User.username == username)
    )
    return user.scalar_one_or_none()


async def create_user(session: AsyncSession, user_in: UserCreate):
    password = str(hash_password(user_in.password))
    data = user_in.model_dump(exclude={"password"})
    user = User(**data, password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_token(session: AsyncSession, user_in: UserLogin):
    user = (
        await session.execute(
            select(User)
            .options(load_only(User.id, User.username, User.name))
            .filter(User.username == user_in.username)
        )
    ).scalar_one_or_none()
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


def decode_token(session: AsyncSession, token: str):
    return jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALGORITHM])


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
