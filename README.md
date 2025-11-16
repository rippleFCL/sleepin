# Sleepin

A FastAPI project with SQLite database and Alembic migrations.

## Setup

### Prerequisites

- Python 3.10+
- Poetry

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Initialize the database:
```bash
poetry run alembic upgrade head
```

3. Run the development server:
```bash
poetry run uvicorn sleepin.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## Database Migrations

### Create a new migration

```bash
poetry run alembic revision --autogenerate -m "description of changes"
```

### Apply migrations

```bash
poetry run alembic upgrade head
```

### Rollback migration

```bash
poetry run alembic downgrade -1
```

## Project Structure

```
sleepin/
├── sleepin/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database configuration
│   └── models/          # SQLAlchemy models
├── alembic/             # Database migrations
├── pyproject.toml       # Poetry configuration
└── README.md
```
