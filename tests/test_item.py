def test_items(client_auth):
    response = client_auth.get("/api/v1/items")
    assert response.status_code == 200
