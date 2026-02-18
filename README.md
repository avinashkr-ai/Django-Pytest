# Django Authentication & CRUD REST API with Pytest

This project implements a simple Django REST API with:

- JWT-based authentication (using SimpleJWT)
- User registration
- Protected CRUD operations for a `Task` model
- Automated tests written with Pytest

## Requirements

- Python 3.9+
- Virtual environment tool (`venv`, `pipenv`, or `poetry`)

## Setup (one time)

1. **Create and activate virtualenv**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create your `.env` from the example**

   ```bash
   cp example.env .env
   ```

   Then edit `.env` to set:

   - **`DJANGO_SECRET_KEY`**: strong 32+ character secret (used for Django & JWT)
   - **`DJANGO_DEBUG`**: `1` for development, `0` for production-like

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

## Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API overview (what this project provides)

- `POST /api/auth/register/` – Register a new user
- `POST /api/auth/token/` – Obtain JWT access/refresh tokens
- `POST /api/auth/token/refresh/` – Refresh access token
- `GET /api/tasks/` – List authenticated user's tasks
- `POST /api/tasks/` – Create a new task
- `GET /api/tasks/<id>/` – Retrieve a task
- `PUT /api/tasks/<id>/` – Update a task
- `DELETE /api/tasks/<id>/` – Delete a task

All `/api/tasks/` endpoints require a valid `Authorization: Bearer <access_token>` header.

### Data model

- **User**: standard Django `User` model (username, email, password, etc.).
- **Task**:
  - `id`, `title`, `description`, `is_completed`
  - `created_at`, `updated_at`
  - `owner` (FK to `User`)

Only the `owner` can see and modify their own tasks.

### Project structure (high level)

- `config/` – Django project, settings, URLs, ASGI/WSGI
- `apps/users/` – registration serializer, API view, URLs
- `apps/tasks/` – `Task` model, serializer, viewset, URLs
- `tests/` – Pytest tests for auth and tasks
- `pytest.ini` – Pytest + coverage configuration

### API schema & Postman / Swagger

This project uses **drf-spectacular** to auto-generate an OpenAPI (Swagger) schema.

When the server is running:

- **Raw OpenAPI schema (JSON)**:  
  `GET http://127.0.0.1:8000/api/schema/`
- **Interactive Swagger UI docs**:  
  `GET http://127.0.0.1:8000/api/docs/`

You can use these in two ways:

- **For Postman**:
  - Open Postman → **Import**
  - Choose **Link**
  - Paste: `http://127.0.0.1:8000/api/schema/`
  - Postman will create a collection with all endpoints.

- **To generate a `swagger.json` file (optional)**:
  - With your virtualenv active:

    ```bash
    python manage.py spectacular --format openapi-json --file swagger.json
    ```

  - This writes a `swagger.json` file based on your current API code.

### Example API code

**User registration endpoint** (`apps/users/views.py`):

```python
from rest_framework import generics, permissions

from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Simple user registration endpoint.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
```

This view:

- accepts `POST /api/auth/register/` with `username`, `email`, `password`
- uses a serializer to validate data and create a new `User`
- allows **anyone** (even not logged in) to call it

**Task CRUD endpoint** (`apps/tasks/views.py`):

```python
from rest_framework import permissions, viewsets

from .models import Task
from .serializers import TaskSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.owner == request.user


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

This viewset:

- requires the user to be **authenticated**
- only returns tasks belonging to the current user
- automatically sets `owner` when a new task is created

## Run tests

```bash
pytest
```

### Coverage and `pytest.ini`

`pytest.ini` configures:

- **Django settings** for tests: `DJANGO_SETTINGS_MODULE = config.settings`
- **Which test files to discover**: `python_files = tests.py test_*.py`
- **Default options**:
  - run with Django settings
  - reuse the test database
  - measure coverage for `apps` and `config`
  - use this same `pytest.ini` as Coverage config (so coverage respects its `omit` rules)
- **Coverage omit rules** (under `[coverage:run]`) to ignore framework boilerplate like `config/asgi.py` and `config/wsgi.py` in reports.

You can see a coverage report in the terminal with:

```bash
pytest --cov=apps --cov=config --cov-report=term-missing
```

### How Pytest works in this project (beginner-friendly)

Pytest discovers tests in the `tests/` folder. Some important pieces:

- **Fixtures in `tests/conftest.py`**:

  ```python
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
  ```

  - `api_client` gives you a DRF `APIClient` to call your API in tests.
  - `user` creates a test user in the database (Pytest provides the `db` fixture).

- **Authenticated client fixture**:

  ```python
  @pytest.fixture
  def auth_client(api_client: APIClient, user: User) -> APIClient:
      response = api_client.post(
          "/api/auth/token/",
          {"username": "testuser", "password": "strong-password"},
          format="json",
      )
      access = response.data["access"]
      api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
      return api_client
  ```

  This fixture:

  - logs in with the test user
  - gets a JWT `access` token
  - attaches it to the client as `Authorization: Bearer <token>`
  - returns a client that acts like a logged-in user

- **Example test for registration** (`tests/test_auth.py`):

  ```python
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
  ```

  - `@pytest.mark.django_db` tells Pytest this test uses the database.
  - the test calls the registration API and then checks:
    - HTTP status is 201 (Created)
    - a new `User` was actually saved.

- **Example test for task creation** (`tests/test_tasks.py`):

  ```python
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
  ```

  - uses `auth_client` so the request is authenticated
  - posts data to create a task
  - checks that the response is 201 and that the returned data matches what we expect.

In summary, you:

1. Write tests that call your API endpoints using reusable fixtures.
2. Use simple `assert` statements to describe what should happen.
3. Run `pytest` and let it handle setup/teardown of the test database and Django environment for you.


