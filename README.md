# Django Authentication & CRUD REST API with Pytest

This project implements a simple Django REST API with:

- JWT-based authentication (using SimpleJWT)
- User registration
- Protected CRUD operations for a `Task` model
- Automated tests written with Pytest

## Requirements

- Python 3.9+
- Virtual environment tool (`venv`, `pipenv`, or `poetry`)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create your `.env` from the provided example (recommended; also avoids JWT key-length warnings):

```bash
cp example.env .env
```

Apply migrations:

```bash
python manage.py migrate
```

## Running the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Overview

- `POST /api/auth/register/` – Register a new user
- `POST /api/auth/token/` – Obtain JWT access/refresh tokens
- `POST /api/auth/token/refresh/` – Refresh access token
- `GET /api/tasks/` – List authenticated user's tasks
- `POST /api/tasks/` – Create a new task
- `GET /api/tasks/<id>/` – Retrieve a task
- `PUT /api/tasks/<id>/` – Update a task
- `DELETE /api/tasks/<id>/` – Delete a task

All `/api/tasks/` endpoints require a valid `Authorization: Bearer <access_token>` header.

## Running Tests

```bash
pytest
```

Coverage configuration is included via `pytest.ini`. You can also see a coverage report in the terminal:

```bash
pytest --cov=apps --cov=config --cov-report=term-missing
```

