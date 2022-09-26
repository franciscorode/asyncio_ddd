# ⚡ Asyncio DDD

Example project using asyncio and DDD patterns

## 💻 Set up

1. 🐱 Get the repository

```shell
git clone git@github.com:imageneratext/asyncio_ddd.git
```

2. 🏗️ Create a virtual environment (e.g. with virtualenv)

```shell
python3.10 -m venv venv
. venv/bin/activate
```

3. 📥 Install the dependencies

```shell
make install
```

4. 🔛 Enable pre-commit hooks

```shell
pre-commit install
```

### 💾 DB migrations management

- Database changes are managed with ⚗️ [alembic](https://alembic.sqlalchemy.org/en/latest/), for more ℹ️ details see [README](asyncio_ddd/shared/infrastructure/persistence/migrations/README.md)

## ✔️ Test

```shell
make test
```

## 🧹 Lint

The configured linters are:

- pylint
- flake8
- mypy

```shell
make lint
```

## 🌟 Format

```shell
make format
```
