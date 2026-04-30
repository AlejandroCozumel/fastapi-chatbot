def _token(client):
    client.post(
        "/auth/register",
        json={"username": "emailuser", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": "emailuser", "password": "password123"},
    )
    return response.json()["access_token"]


def test_email_draft_contract(client):
    token = _token(client)

    response = client.post(
        "/email/drafts",
        json={
            "recipient": "person@example.com",
            "subject": "Hello",
            "body": "Message body",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["recipient"] == "person@example.com"
    assert body["status"] == "draft"


def test_email_send_contract(client):
    token = _token(client)
    draft = client.post(
        "/email/drafts",
        json={
            "recipient": "person@example.com",
            "subject": "Hello",
            "body": "Message body",
        },
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    response = client.post(
        f"/email/drafts/{draft['id']}/send",
        json={
            "confirm": True,
            "recipient": "person@example.com",
            "subject": "Hello",
            "body": "Message body",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "sent"
