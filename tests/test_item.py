from app.models import Item, StatusEnum


def get_by_title(title: str, db_session):
    return db_session.query(Item).filter(Item.title == title).first()


def test_create_item(client_auth):
    response = client_auth.post(
        "/api/v1/items", json={"title": "test", "description": "test"}
    )
    assert response.status_code == 200


def test_items(client_auth):
    response = client_auth.get("/api/v1/items")
    assert response.status_code == 200


def test_get_item(client_auth, db_session):
    item = get_by_title("test", db_session)
    response = client_auth.get(f"/api/v1/items/{item.id}")
    assert response.status_code == 200


def test_get_item_404(client_auth, db_session):
    response = client_auth.get(f"/api/v1/items/10")
    assert response.status_code == 404


def test_update_item(client_auth, db_session):
    item = get_by_title("test", db_session)
    response = client_auth.put(
        f"/api/v1/items/{item.id}", json={"title": "test_update", "description": "test"}
    )
    assert response.status_code == 200


def test_update_item_status(client_auth, db_session):
    item = get_by_title("test_update", db_session)
    assert item.status == StatusEnum.pending
    response = client_auth.patch(
        f"/api/v1/items/{item.id}", json={"status": "completed"}
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == StatusEnum.completed.value


def test_delete_item(client_auth, db_session):
    item = get_by_title("test_update", db_session)
    response = client_auth.delete(f"/api/v1/items/{item.id}")
    assert response.status_code == 200
    assert get_by_title("test_update", db_session) == None
