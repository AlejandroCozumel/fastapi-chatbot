from unittest.mock import patch


def _token(client, username="docsflow"):
    client.post(
        "/auth/register",
        json={"username": username, "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": username, "password": "password123"},
    )
    return response.json()["access_token"]


def test_upload_and_document_grounded_answer(client):
    token = _token(client)
    upload = client.post(
        "/documents",
        files={
            "file": (
                "policy.txt",
                b"The refund window is 30 days for local purchases.",
                "text/plain",
            )
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert upload.status_code == 201

    with patch("app.services.rag.get_assistant_response", return_value="30 days"):
        response = client.post(
            "/documents/query",
            json={"question": "What is the refund window?"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    assert response.json()["answer"] == "30 days"
    assert "refund window" in response.json()["context"]


def test_missing_documents_returns_404(client):
    token = _token(client, "missingdocs")

    response = client.post(
        "/documents/query",
        json={"question": "What is in my files?"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert "document context" in response.json()["detail"]


def test_unsupported_upload_is_rejected(client):
    token = _token(client, "badupload")

    response = client.post(
        "/documents",
        files={"file": ("image.png", b"not text", "image/png")},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported document type"


def test_document_query_is_user_isolated(client):
    owner_token = _token(client, "docowner")
    other_token = _token(client, "docother")
    client.post(
        "/documents",
        files={"file": ("private.txt", b"Private project code is ABC.", "text/plain")},
        headers={"Authorization": f"Bearer {owner_token}"},
    )

    response = client.post(
        "/documents/query",
        json={"question": "What is the project code?"},
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 404
