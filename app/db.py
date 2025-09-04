from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.config import settings
from collections.abc import Generator
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> Generator[AsyncSession, None, None]:
    async with async_session_maker() as session:
        yield session
