import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_user_can_register(api_client):
    payload = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "super-strong-password",
    }
    response = api_client.post("/api/auth/register/", payload, format="json")

    assert response.status_code == 201
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_user_can_obtain_jwt_token(api_client, user):
    response = api_client.post(
        "/api/auth/token/",
        {"username": "testuser", "password": "strong-password"},
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

