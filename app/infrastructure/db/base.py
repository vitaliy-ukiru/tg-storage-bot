__all__ = (
    'Base',
    'DSN'
)

from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# TODO: replaces with env config
# It is localhost data only for testing and migrations
DSN = URL.create(
    drivername="postgresql+asyncpg",
    username="py-tg",
    password="py-tg",
    host="localhost",
    database="tg-storage"
)
