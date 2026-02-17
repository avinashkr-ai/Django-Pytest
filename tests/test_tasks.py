import pytest


@pytest.mark.django_db
def test_cannot_access_tasks_without_auth(api_client):
    response = api_client.get("/api/tasks/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_task(auth_client):
    payload = {
        "title": "My Task",
        "description": "Do something important",
    }
    response = auth_client.post("/api/tasks/", payload, format="json")

    assert response.status_code == 201
    assert response.data["title"] == "My Task"
    assert response.data["is_completed"] is False


@pytest.mark.django_db
def test_list_only_own_tasks(auth_client, task_factory, user, db):
    # Create a task for authenticated user
    task_factory(title="User Task")

    # Create a task for another user
    from apps.tasks.models import Task
    from django.contrib.auth import get_user_model

    OtherUser = get_user_model()
    other = OtherUser.objects.create_user(
        username="other",
        email="other@example.com",
        password="strong-password",
    )
    Task.objects.create(title="Other Task", description="x", owner=other)

    response = auth_client.get("/api/tasks/")
    assert response.status_code == 200
    titles = [item["title"] for item in response.data]
    assert "User Task" in titles
    assert "Other Task" not in titles


@pytest.mark.django_db
def test_update_task(auth_client, task_factory):
    task = task_factory(title="Old title")
    url = f"/api/tasks/{task.id}/"
    response = auth_client.put(
        url,
        {"title": "New title", "description": task.description, "is_completed": True},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["title"] == "New title"
    assert response.data["is_completed"] is True


@pytest.mark.django_db
def test_delete_task(auth_client, task_factory):
    task = task_factory()
    url = f"/api/tasks/{task.id}/"
    response = auth_client.delete(url)
    assert response.status_code == 204

