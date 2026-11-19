"""API tests: health, system diagnostics, and project CRUD."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/system/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_create_and_list_project():
    payload = {
        "name": "Test Project",
        "source_title": "Sample Video",
        "source_creator": "Test Creator",
        "language": "en",
    }
    response = client.post("/api/projects", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["id"]

    project_id = data["id"]

    # List
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert any(p["id"] == project_id for p in response.json())

    # Get
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id

    # Update
    response = client.patch(f"/api/projects/{project_id}", json={"name": "Renamed Project"})
    assert response.status_code == 200
    assert response.json()["name"] == "Renamed Project"

    # Delete (soft delete)
    response = client.delete(f"/api/projects/{project_id}")
    assert response.status_code == 204

    # Verify soft-deleted project no longer appears in list
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert not any(p["id"] == project_id for p in response.json())


def test_create_project_invalid_url():
    response = client.post(
        "/api/projects",
        json={"name": "Bad", "source_url": "../../etc/passwd"},
    )
    assert response.status_code == 400 or response.status_code == 422


def test_get_nonexistent_project():
    response = client.get("/api/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
