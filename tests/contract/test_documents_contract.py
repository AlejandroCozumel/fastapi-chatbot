def _token(client):
    client.post(
        "/auth/register",
        json={"username": "docsuser", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": "docsuser", "password": "password123"},
    )
    return response.json()["access_token"]


def test_document_upload_contract(client):
    token = _token(client)

    response = client.post(
        "/documents",
        files={"file": ("notes.txt", b"FastAPI supports local APIs.", "text/plain")},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["filename"] == "notes.txt"
    assert body["status"] == "processed"


def test_document_query_contract(client):
    token = _token(client)
    client.post(
        "/documents",
        files={"file": ("notes.txt", b"SQLite stores local data.", "text/plain")},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.post(
        "/documents/query",
        json={"question": "Where is data stored?"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert body["document_ids"]
