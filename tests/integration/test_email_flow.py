from unittest.mock import patch


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


def _draft(client, token):
    return client.post(
        "/email/drafts",
        json={
            "recipient": "person@example.com",
            "subject": "Status",
            "body": "Everything is ready.",
        },
        headers={"Authorization": f"Bearer {token}"},
    ).json()


def test_draft_creation_and_successful_send(client):
    token = _token(client, "emailsuccess")
    draft = _draft(client, token)

    with patch("app.services.email._send_with_resend", return_value="msg_123"):
        response = client.post(
            f"/email/drafts/{draft['id']}/send",
            json={
                "confirm": True,
                "recipient": draft["recipient"],
                "subject": draft["subject"],
                "body": draft["body"],
            },
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "sent"
    assert response.json()["provider_message_id"] == "msg_123"


def test_confirmation_mismatch_blocks_send(client):
    token = _token(client, "emailmismatch")
    draft = _draft(client, token)

    response = client.post(
        f"/email/drafts/{draft['id']}/send",
        json={
            "confirm": True,
            "recipient": draft["recipient"],
            "subject": "Changed",
            "body": draft["body"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Confirmation does not match draft"


def test_unconfirmed_send_is_blocked(client):
    token = _token(client, "emailunconfirmed")
    draft = _draft(client, token)

    response = client.post(
        f"/email/drafts/{draft['id']}/send",
        json={
            "confirm": False,
            "recipient": draft["recipient"],
            "subject": draft["subject"],
            "body": draft["body"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Explicit confirmation is required"


def test_failed_resend_call_is_recorded(client):
    token = _token(client, "emailfail")
    draft = _draft(client, token)

    with patch("app.services.email._send_with_resend", side_effect=RuntimeError("boom")):
        response = client.post(
            f"/email/drafts/{draft['id']}/send",
            json={
                "confirm": True,
                "recipient": draft["recipient"],
                "subject": draft["subject"],
                "body": draft["body"],
            },
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert response.json()["error_message"] == "boom"
