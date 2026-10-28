
import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks():
    # Give every test a clean, predictable starting state.
    main.tasks.clear()
    main.task_ids = iter(range(1, 1_000_000))
    yield
    main.tasks.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_tasks_returns_empty_list():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn JMeter",
            "description": "Build my first performance test",
            "completed": False,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Learn JMeter",
        "description": "Build my first performance test",
        "completed": False,
    }


def test_get_existing_task():
    created = client.post(
        "/tasks",
        json={"title": "Write test plan"},
    )
    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Write test plan"


def test_get_missing_task_returns_404():
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():
    created = client.post(
        "/tasks",
        json={"title": "Original title"},
    )
    task_id = created.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["completed"] is True


def test_update_missing_task_returns_404():
    response = client.put(
        "/tasks/999",
        json={"title": "Missing task"},
    )

    assert response.status_code == 404


def test_delete_task():
    created = client.post(
        "/tasks",
        json={"title": "Task to delete"},
    )
    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_delete_missing_task_returns_404():
    response = client.delete("/tasks/999")

    assert response.status_code == 404


def test_create_task_rejects_missing_title():
    response = client.post(
        "/tasks",
        json={"description": "A title is required"},
    )

    assert response.status_code == 422


def test_create_task_rejects_empty_title():
    response = client.post(
        "/tasks",
        json={"title": ""},
    )

    assert response.status_code == 422
