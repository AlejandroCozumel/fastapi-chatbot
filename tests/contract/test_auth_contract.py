def test_register_contract(client):
    response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "password123"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert "password" not in body
    assert "password_hash" not in body


def test_login_contract(client):
    client.post("/auth/register", json={"username": "bob", "password": "password123"})

    response = client.post(
        "/auth/login",
        json={"username": "bob", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
