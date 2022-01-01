from fastapi.testclient import TestClient


def test_auth(client_secure: TestClient):
    response = client_secure.get("/api/?token=test:pass")
    assert response.status_code == 200

    response = client_secure.get("/api/", auth=("test", "pass"))
    assert response.status_code == 200

    response = client_secure.get("/api/?token=test:pass", auth=("test", "pass"))
    assert response.status_code == 200


def test_auth_key_fail(client_secure: TestClient):
    response = client_secure.get("/api/?token=pirate:pass")
    assert response.status_code == 401

    response = client_secure.get("/api/", auth=("pirate", "pass"))
    assert response.status_code == 401

    response = client_secure.get("/api/?token=pirate:pass", auth=("pirate", "pass"))
    assert response.status_code == 401


def test_auth_key_invalid(client_secure: TestClient):
    response = client_secure.get("/api/?token=pirate::pass")
    assert response.status_code == 401

    response = client_secure.get("/api/", auth=("pirate:", "pass"))
    assert response.status_code == 401

    response = client_secure.get("/api/?token=pirate::pass:", auth=("pirate", "pass"))
    assert response.status_code == 401


def test_create_endpoint(client):
    response = client.post(
        "/api/",
        json={
            "url": "http://example.com",
            "method": "POST",
            "timeout": 10,
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "uid": "0ea967fc-efa2-5bd3-9d4d-031779b04921",
        "url": "http://example.com",
        "method": "POST",
        "timeout": 10,
        "call": None,
    }


def test_list_endpoints(client):
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        "/api/",
        json={
            "url": "http://example.com",
            "method": "POST",
            "timeout": 10,
        },
    )
    assert response.status_code == 201

    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "uid": "0ea967fc-efa2-5bd3-9d4d-031779b04921",
            "url": "http://example.com",
            "method": "POST",
            "timeout": 10,
            "call": None,
        }
    ]


def test_delete_endpoint(client):
    response = client.post(
        "/api/",
        json={
            "url": "http://example.com",
            "method": "POST",
            "timeout": 10,
        },
    )
    assert response.status_code == 201
    response = client.delete("/api/0ea967fc-efa2-5bd3-9d4d-031779b04921")
    assert response.status_code == 200
