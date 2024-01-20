Generic single-database configuration with an async dbapi.


## New revision
```
alembic revision --autogenerate -m "message"
```

## Migrations
```
alembic upgrade +1
```

to head
```
alembic upgrade head
```

for rollback
```
alembic downgrade -1
```

### Provide config path via env var or alembic.ini
example
```
CONFIG_PATH=your/path/config.yaml alembic upgrade +1
```
