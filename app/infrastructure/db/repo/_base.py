from typing import Optional, Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.domain.dto.common import Pagination
from app.core.interfaces.repository.common import FilterField
from app.infrastructure.db.repo.filters.container import Container


class BaseRepository:
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    @staticmethod
    def apply_filters(stmt: Select, reg: Container, filters: Sequence[FilterField]) -> Select:
        for f in filters:
            stmt = stmt.where(reg.convert(f))
        return stmt

    @staticmethod
    def apply_pagination(stmt: Select, p: Optional[Pagination]) -> Select:
        if p is None:
            return stmt
        if p.limit is not None:
            stmt = stmt.limit(p.limit)
        if p.offset is not None:
            stmt = stmt.offset(p.offset)

        return stmt
