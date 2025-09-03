import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models import Base
from app.db import get_session
from app.services.user import create_user, get_token
from app.dto import UserCreate, UserLogin

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_db
    yield TestClient(app)


user = UserCreate(username="default-user-test", password="test", name="test")


@pytest.fixture(scope="session")
def default_user(db_session):
    yield create_user(db_session, user)


@pytest.fixture
def client_auth(client, default_user, db_session):
    token = get_token(db_session, user)
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client
