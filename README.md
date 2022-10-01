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
make test
```

## 🧹 Lint

The current linters are [pylint](https://github.com/PyCQA/pylint), [flake8](https://github.com/PyCQA/flake8) and [mypy](https://github.com/python/mypy)

```shell
make lint
```

## 🌟 Format

The current code formatters are [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort)

```shell
make format
```
