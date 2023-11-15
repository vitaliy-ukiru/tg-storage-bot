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
    username="tg-storage-bot",
    password="tg-storage-bot",
    database="py-tg-fs-bot"
)
