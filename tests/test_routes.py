import pytest
from datetime import date, timedelta
import app.routes
from app.repository import TaskRepository
from app.service import TaskService

@pytest.fixture
def client():
    test_app = app.routes.app
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        # Use in-memory SQLite
        repo = TaskRepository(":memory:")
        # Replace the service in routes module
        app.routes.service = TaskService(repo)
        yield client

def test_welcome_endpoint(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data
    assert "endpoints" in data
    assert data["version"] == "1.0.0"
    assert "GET /tasks" in data["endpoints"]

def test_create_task(client):
    tomorrow = date.today() + timedelta(days=1)
    resp = client.post("/tasks", json={"title": "Test", "due_date": tomorrow.isoformat()})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "Test"
    assert data["id"] is not None

def test_create_task_invalid_title(client):
    resp = client.post("/tasks", json={"title": "", "due_date": "2025-12-12"})
    assert resp.status_code == 400

def test_create_task_past_due_date(client):
    yesterday = date.today() - timedelta(days=1)
    resp = client.post("/tasks", json={"title": "x", "due_date": yesterday.isoformat()})
    assert resp.status_code == 400

def test_toggle_existing_task(client):
    tomorrow = date.today() + timedelta(days=1)
    create_resp = client.post("/tasks", json={"title": "Toggle", "due_date": tomorrow.isoformat()})
    task_id = create_resp.get_json()["id"]

    resp = client.patch(f"/tasks/{task_id}/toggle")
    assert resp.status_code == 200
    assert resp.get_json()["completed"] is True

def test_toggle_non_existent_task(client):
    resp = client.patch("/tasks/9999/toggle")
    assert resp.status_code == 404

def test_get_all_tasks_empty(client):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_get_all_tasks_with_data(client):
    tomorrow = date.today() + timedelta(days=1)
    client.post("/tasks", json={"title": "Task 1", "due_date": tomorrow.isoformat()})
    client.post("/tasks", json={"title": "Task 2", "due_date": tomorrow.isoformat()})
    
    resp = client.get("/tasks")
    assert resp.status_code == 200
    tasks = resp.get_json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"

def test_get_single_task(client):
    tomorrow = date.today() + timedelta(days=1)
    create_resp = client.post("/tasks", json={"title": "Single", "due_date": tomorrow.isoformat()})
    task_id = create_resp.get_json()["id"]
    
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    task = resp.get_json()
    assert task["title"] == "Single"
    assert task["id"] == task_id

def test_get_non_existent_task(client):
    resp = client.get("/tasks/9999")
    assert resp.status_code == 404
    assert "error" in resp.get_json()

def test_delete_task(client):
    tomorrow = date.today() + timedelta(days=1)
    create_resp = client.post("/tasks", json={"title": "Delete", "due_date": tomorrow.isoformat()})
    task_id = create_resp.get_json()["id"]
    
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Task deleted"
    
    # Verify it's deleted
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404

def test_delete_non_existent_task(client):
    resp = client.delete("/tasks/9999")
    assert resp.status_code == 404
    assert "error" in resp.get_json()