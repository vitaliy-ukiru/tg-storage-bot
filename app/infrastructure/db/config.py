from app.common.config.config import DbConfig
from sqlalchemy import URL

def to_dsn(cfg: DbConfig) -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        username=cfg.username,
        password=cfg.password,
        database=cfg.database,
        host=cfg.host,
        port=cfg.port,
    )

