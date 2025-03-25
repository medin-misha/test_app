#!/bin/bash

export postgres_host=postgres/postgres_db
export postgres_user=postgres_user
export postgres_password=postgres_password
export currencylayer_key=8e20b54761b122c5f1af35d195a82292


uv run alembic revision --autogenerate -m "migrations"
uv run alembic upgrade head
uv run gunicorn main:app --workers 33 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000