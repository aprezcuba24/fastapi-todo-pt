import pytest
from app.models import Item, StatusEnum


@pytest.mark.asyncio_cooperative
async def test_create_item(client_auth):
    response = await client_auth.post(
        "/items", json={"title": "test", "description": "test"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio_cooperative
async def test_items(client_auth):
    await client_auth.post("/items", json={"title": "test", "description": "test"})
    response = await client_auth.get("/items")
    assert response.status_code == 200
    assert response.json()["total"] == 1


@pytest.mark.asyncio_cooperative
async def test_get_item(client_auth):
    response = await client_auth.post(
        "/items", json={"title": "test", "description": "test"}
    )
    item = response.json()
    response = await client_auth.get(f"/items/{item['id']}")
    assert response.status_code == 200


@pytest.mark.asyncio_cooperative
async def test_get_item_404(client_auth, db_session):
    response = await client_auth.get(f"/items/10")
    assert response.status_code == 404


@pytest.mark.asyncio_cooperative
async def test_update_item(client_auth, db_session):
    response = await client_auth.post(
        "/items", json={"title": "test", "description": "test"}
    )
    item = response.json()
    response = await client_auth.put(
        f"/items/{item['id']}", json={"title": "test_update", "description": "test"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "test_update"
    assert response.json()["description"] == "test"


@pytest.mark.asyncio_cooperative
async def test_update_item_status(client_auth, db_session):
    response = await client_auth.post(
        "/items", json={"title": "test", "description": "test"}
    )
    item = response.json()
    assert item["status"] == StatusEnum.pending.value
    response = await client_auth.patch(
        f"/items/{item['id']}", json={"status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == StatusEnum.completed.value


@pytest.mark.asyncio_cooperative
async def test_delete_item(client_auth, db_session):
    response = await client_auth.post(
        "/items", json={"title": "test", "description": "test"}
    )
    item = response.json()
    response = await client_auth.delete(f"/items/{item['id']}")
    assert response.status_code == 200
    response = await client_auth.get("/items")
    assert response.status_code == 200
    assert response.json()["total"] == 0
