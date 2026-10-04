# Alembic Commands Cheat Sheet

## Initialize Alembic

```bash
alembic init alembic
```

## Create a Migration

Generate a migration from changes to your SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the change"
```

Example:

```bash
alembic revision --autogenerate -m "add created_at to posts"
```

Migration files are created in:

```text
alembic/versions/
```

## Apply Migrations

Apply all pending migrations:

```bash
alembic upgrade head
```

## Check Current Revision

```bash
alembic current
```

## View Migration History

```bash
alembic history
```

## Roll Back One Migration

```bash
alembic downgrade -1
```

## Roll Back to a Specific Revision

```bash
alembic downgrade <revision_id>
```

Example:

```bash
alembic downgrade 99e2e66db259
```

## Upgrade to a Specific Revision

```bash
alembic upgrade <revision_id>
```

Example:

```bash
alembic upgrade 99e2e66db259
```

## Preview SQL

Show the SQL Alembic would execute without changing the database:

```bash
alembic upgrade head --sql
```

## Normal Development Workflow

After changing `models.py`:

```bash
alembic revision --autogenerate -m "describe the change"
```

Inspect the generated migration.

Then:

```bash
alembic upgrade head
```

Verify:

```bash
alembic current
```

## First Migration

```bash
alembic revision --autogenerate -m "create users and posts tables"
alembic upgrade head
alembic current
```

## Important

Do **not** use:

```python
Base.metadata.create_all(bind=engine)
```

Alembic now manages the database schema.

The workflow is:

```text
models.py
    ↓
alembic revision --autogenerate
    ↓
migration file
    ↓
alembic upgrade head
    ↓
database
```

## Roll back the last migration

```bash
alembic downgrade -1
```

```text

for example 

99e2e66  create users and posts tables
      ↓
abc1234  add created_at to posts

If you're currently at abc1234:

alembic downgrade -1

99e2e66
```