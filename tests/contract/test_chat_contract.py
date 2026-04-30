def _token(client, username="chatuser"):
    client.post(
        "/auth/register",
        json={"username": username, "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": username, "password": "password123"},
    )
    return response.json()["access_token"]


def test_chat_contract(client):
    token = _token(client)

    response = client.post(
        "/chat",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["conversation_id"], int)
    assert body["message"]["role"] == "assistant"
    assert "content" in body["message"]


def test_conversation_history_contract(client):
    token = _token(client, "historyuser")
    chat_response = client.post(
        "/chat",
        json={"message": "Remember this"},
        headers={"Authorization": f"Bearer {token}"},
    )
    conversation_id = chat_response.json()["conversation_id"]

    list_response = client.get(
        "/conversations",
        headers={"Authorization": f"Bearer {token}"},
    )
    detail_response = client.get(
        f"/conversations/{conversation_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert detail_response.json()["messages"][0]["role"] == "user"
