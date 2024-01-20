from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from app.common.config import Config, DatabaseConfig


def connect_db(cfg: Config) -> AsyncEngine:
    engine = create_async_engine(to_dsn(cfg.db), echo=cfg.is_debug)
    return engine

def new_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)


def to_dsn(cfg: DatabaseConfig) -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        username=cfg.username,
        password=cfg.password.get_secret_value() if cfg.password else None,
        database=cfg.database,
        host=cfg.host,
        port=cfg.port,
    )
