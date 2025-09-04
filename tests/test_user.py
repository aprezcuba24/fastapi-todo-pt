import pytest
from httpx import AsyncClient


@pytest.mark.asyncio_cooperative
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users",
        json={"username": "testuser", "password": "testpass", "name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio_cooperative
async def test_create_duplicate_user(client: AsyncClient):
    await client.post(
        "/users",
        json={
            "username": "duplicate",
            "password": "testpass",
            "name": "Duplicate User",
        },
    )
    response = await client.post(
        "/users",
        json={
            "username": "duplicate",
            "password": "testpass",
            "name": "Duplicate User",
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio_cooperative
async def test_login_success(client: AsyncClient):
    await client.post(
        "/users",
        json={"username": "loginuser", "password": "loginpass", "name": "Login User"},
    )
    response = await client.post(
        "/users/login", json={"username": "loginuser", "password": "loginpass"}
    )
    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.asyncio_cooperative
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        "/users/login", json={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
