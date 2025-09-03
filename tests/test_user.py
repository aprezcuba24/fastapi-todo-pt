def test_create_user(client):
    response = client.post(
        "/api/v1/users", json={"username": "test", "password": "1234", "name": "Tester"}
    )
    assert response.status_code == 200


def test_create_user_400(client):
    response = client.post(
        "/api/v1/users", json={"username": "test", "password": "1234", "name": "Tester"}
    )
    assert response.status_code == 400
