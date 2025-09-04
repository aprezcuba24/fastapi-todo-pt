from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import Session
from collections.abc import Generator

engine = create_engine(
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
