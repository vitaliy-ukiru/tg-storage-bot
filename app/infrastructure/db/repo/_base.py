from typing import Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.domain.dto.common import Pagination


class BaseRepository:
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    @staticmethod
    def apply_pagination(stmt: Select, p: Optional[Pagination]) -> Select:
        if p is None:
            return stmt

        if p.limit is not None:
            stmt = stmt.limit(p.limit)
        if p.offset is not None:
            stmt = stmt.offset(p.offset)

        return stmt
