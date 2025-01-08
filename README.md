# ⚡ Asyncio DDD

Example project using asyncio and DDD patterns

## 💡 Motivation

🎓 Consolidate next patterns and technologies

- 📦 Asyncio python libraries: fastapi, SQLAlchemy, alembic, aio-pika, etc
- ♻️ Patterns: SOLID, DDD, CQRS and Event sourcing

## 💻 Set up

1. 🐱 Get the repository

```shell
git clone git@github.com:imageneratext/asyncio_ddd.git
```

2. 🏗️ Create a virtual environment

```shell
poetry shell
```

3. 📥 Install the dependencies

```shell
poetry install
```

4. 🔛 Enable pre-commit hooks

```shell
pre-commit install
```

## 🌎 Create .env file with next variables

- POSTGRES_DB_NAME
- POSTGRES_USER
- POSTGRES_PASSWORD
- PGPASSWORD
- EXTERNAL_POSTGRES_PORT
- APP_ENVIRONMENT
- ALEMBIC_CONFIG

## 🚀 Start application

```shell
make run
```

## 🌐 Web pages

- [⚙️ Admin page](http://0.0.0.0:8000/admin/)
- [📗 Api Swagger page](http://0.0.0.0:8000/docs/)
- [📘 Api Redoc page](http://0.0.0.0:8000/redoc/)

## 💾 DB migrations management

- Database changes are managed with ⚗️ [alembic](https://alembic.sqlalchemy.org/en/latest/), for more ℹ️ details see [README](asyncio_ddd/shared/infrastructure/persistence/migrations/README.md)

## ✔️ Test

```shell
make up
make test
```

## 🧹 Lint

The current linters are [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy)

```shell
make lint
```

## 🌟 Format

The current code formatter is [black](https://github.com/psf/black)

```shell
make format
```
