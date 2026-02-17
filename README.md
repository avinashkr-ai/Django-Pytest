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

