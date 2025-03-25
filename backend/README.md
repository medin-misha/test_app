# Backend API для расчёта расходов 💸

Это бэкенд-сервис, который хранит расходы пользователя (в гривнах) и собирает их в XLS-файл, который отправляется пользователю 📊.

## Реализовано:
**Модели:**
- **User** — пользователь, к которому привязаны расходы (Spending)
- **Spending** — расходы

**Views:**
- CRUD-операции с **Spending**
- **BaseAuth** — аутентификация (только с chat_id (пароль))
- Регистрация пользователей
- Выдача XLS-файла за определённый промежуток времени (который задаёт пользователь)

**DevOps:**
- Контейнеризация приложения 🐳
- Запуск с **gunicorn** 🚀

### Стек:
- FastAPI, SQLAlchemy, Gunicorn, Aiohttp, Alembic, Asyncpg, Openpyxl, Pydantic, Pydantic-settings, Ruff, Uvicorn

### Запуск:
Для начала в этой папке нужно создать файл `run.sh`, далее вписать в него следующий код:

```bash
#!/bin/bash

export postgres_host=postgres/postgres_db
export postgres_user=postgres_user
export postgres_password=postgres_password
export currencylayer_key=твой api key от https://currencylayer.com/dashboard

uv run alembic revision --autogenerate -m "migrations"
uv run alembic upgrade head
uv run gunicorn main:app --workers 33 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Это переменные окружения и команды миграций и запуска. Далее тебе следует зайти в директорию выше (там, где находится docker-compose) и прописать команду:

```bash
docker-compose up --build
```

Подожди немного, и всё запустится. Сервер будет доступен по адресу **127.0.0.1:8001** 🌐.

[CurrencyLayer - Конвертер валют](https://currencylayer.com/dashboard) 💱

