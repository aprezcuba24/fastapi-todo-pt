def test_create_item(client_auth):
    response = client_auth.post(
        "/api/v1/items", json={"title": "test", "description": "test"}
    )
    assert response.status_code == 200


def test_items(client_auth):
    response = client_auth.get("/api/v1/items")
    assert response.status_code == 200
