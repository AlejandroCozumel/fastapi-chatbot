def test_registration_login_and_authenticated_me(client):
    register_response = client.post(
        "/auth/register",
        json={"username": "carol", "password": "password123"},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"username": "carol", "password": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "carol"


def test_invalid_login_is_rejected(client):
    client.post("/auth/register", json={"username": "dave", "password": "password123"})

    response = client.post(
        "/auth/login",
        json={"username": "dave", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_missing_token_is_rejected(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing access token"


def test_duplicate_username_is_rejected(client):
    payload = {"username": "erin", "password": "password123"}
    assert client.post("/auth/register", json=payload).status_code == 201

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
