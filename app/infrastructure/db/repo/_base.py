from typing import Optional, Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncSessionTransaction

from app.core.domain.dto.common import Pagination
from app.core.interfaces.repository.common import FilterField
from app.infrastructure.db.models import Base
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

    async def get_count(self,
                        session: AsyncSession,
                        model: type[Base],
                        filters: Sequence[FilterField],
                        reg: Container) -> int:
        stmt = self.apply_filters(
            select(func.count()).select_from(model),
            reg,
            filters
        )

        count = await session.scalar(stmt)
        return count