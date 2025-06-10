# Database Migrations

We use alembic for database migrations. As a package user, see the CLI `sc-audit schema` commands.

As a developer, you can run alembic commands from the ./sc_audit directory.

## Upgrade schema

To migrate your local DB to the latest schema, do:

```sh
alembic upgrade head
```

This command also works when you don't have a local DB yet. It will create the sqlite file for you.

## Revise schema

To bring the DB schema in line with the SQLAlchemy models, you can try autogenerating a migration:

```sh
alembic revision --autogenerate -m "description of schema change"
```

Carefully read the generated migration file and edit it if needed.
