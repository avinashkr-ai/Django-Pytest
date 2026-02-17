import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="strong-password",
    )


@pytest.fixture
def auth_client(api_client: APIClient, user: User) -> APIClient:
    # Obtain JWT token
    response = api_client.post(
        "/api/auth/token/",
        {"username": "testuser", "password": "strong-password"},
        format="json",
    )
    assert response.status_code == 200
    access = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return api_client


@pytest.fixture
def task_factory(user: User):
    from apps.tasks.models import Task

    def factory(**kwargs) -> Task:
        data = {"title": "Sample task", "description": "Desc", "owner": user}
        data.update(kwargs)
        return Task.objects.create(**data)

    return factory

