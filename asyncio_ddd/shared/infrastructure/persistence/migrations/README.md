# ⚗️ DB migrations management with alembic

## ➕ Create migration

```shell
make create-migration m="migration name"
```

☑️ Check migration revision generated in `asyncio_ddd/shared/infrastructure/persistence/migrations/revisions`

## ♻️ Run migrations

```shell
make run-migrations
```
