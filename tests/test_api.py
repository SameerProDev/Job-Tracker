import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.test_client() as client:
        yield client


def make(client, **overrides):
    payload = {"company": "Acme", "role": "Junior Developer", **overrides}
    return client.post("/api/applications", json=payload)


def test_create_application(client):
    res = make(client)
    assert res.status_code == 201
    body = res.get_json()
    assert body["company"] == "Acme"
    assert body["status"] == "applied"


def test_create_requires_company_and_role(client):
    res = client.post("/api/applications", json={"company": ""})
    assert res.status_code == 400
    assert set(res.get_json()["errors"]) == {"company", "role"}


def test_invalid_status_rejected(client):
    assert make(client, status="ghosted").status_code == 400


def test_list_and_filter_by_status(client):
    make(client, company="A")
    make(client, company="B", status="interview")
    assert len(client.get("/api/applications").get_json()) == 2
    filtered = client.get("/api/applications?status=interview").get_json()
    assert [a["company"] for a in filtered] == ["B"]


def test_update_application(client):
    app_id = make(client).get_json()["id"]
    res = client.put(f"/api/applications/{app_id}", json={"status": "offer"})
    assert res.status_code == 200
    assert res.get_json()["status"] == "offer"


def test_delete_application(client):
    app_id = make(client).get_json()["id"]
    assert client.delete(f"/api/applications/{app_id}").status_code == 204
    assert client.get(f"/api/applications/{app_id}").status_code == 404


def test_stats(client):
    make(client)
    make(client, status="offer")
    stats = client.get("/api/stats").get_json()
    assert stats["total"] == 2
    assert stats["by_status"]["offer"] == 1
