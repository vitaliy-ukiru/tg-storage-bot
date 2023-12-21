from sqlalchemy.ext.asyncio import async_sessionmaker


class BaseRepository:
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker
