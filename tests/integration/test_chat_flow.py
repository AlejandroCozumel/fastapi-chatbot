from unittest.mock import patch

import pytest

from app.core.errors import ProviderError


def _token(client, username):
    client.post(
        "/auth/register",
        json={"username": username, "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": username, "password": "password123"},
    )
    return response.json()["access_token"]


def test_chat_persists_user_and_assistant_messages(client):
    token = _token(client, "alice")

    with patch(
        "app.services.conversations.get_assistant_response",
        return_value="Assistant reply",
    ):
        response = client.post(
            "/chat",
            json={"message": "Hello"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    conversation_id = response.json()["conversation_id"]

    detail = client.get(
        f"/conversations/{conversation_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert detail.status_code == 200
    messages = detail.json()["messages"]
    assert [message["role"] for message in messages] == ["user", "assistant"]
    assert messages[1]["content"] == "Assistant reply"


def test_conversation_history_is_user_isolated(client):
    token_a = _token(client, "owner")
    token_b = _token(client, "other")

    response = client.post(
        "/chat",
        json={"message": "Private"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    conversation_id = response.json()["conversation_id"]

    forbidden = client.get(
        f"/conversations/{conversation_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert forbidden.status_code == 404


def test_provider_failure_returns_502_without_losing_history(client):
    token = _token(client, "providerfail")

    with patch(
        "app.services.conversations.get_assistant_response",
        side_effect=ProviderError("OpenAI request failed"),
    ):
        response = client.post(
            "/chat",
            json={"message": "Fail"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 502
    assert response.json()["detail"] == "OpenAI request failed"
    assert client.get(
        "/conversations",
        headers={"Authorization": f"Bearer {token}"},
    ).status_code == 200


def test_chat_requires_authentication(client):
    response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 401
