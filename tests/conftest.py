import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import get_session, async_session_maker, engine
from app.services.user import create_user, get_token, find_by_username
from app.dto import UserCreate


TestingSessionLocal = async_session_maker


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.begin() as connection:
        async with TestingSessionLocal(bind=connection) as session:
            try:
                yield session
            finally:
                await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver/api/v1"
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()


user = UserCreate(username="default-user-test", password="test", name="test")


@pytest_asyncio.fixture
async def default_user(db_session):
    user_db = await find_by_username(db_session, user.username)
    if not user_db:
        user_db = await create_user(db_session, user)
    yield user_db


@pytest_asyncio.fixture
async def client_auth(client, default_user, db_session):
    token = await get_token(db_session, user)
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client
