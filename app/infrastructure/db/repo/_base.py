from typing import Optional, Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncSessionTransaction

from app.core.domain.dto.common import Pagination
from app.core.interfaces.repository.common import FilterField
from app.infrastructure.db.models import Base
from app.infrastructure.db.repo.filters.container import Container
from .utils import apply_filters


class BaseRepository:
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker


    async def get_count(self,
                        session: AsyncSession,
                        model: type[Base],
                        filters: Sequence[FilterField],
                        reg: Container) -> int:
        stmt = apply_filters(
            select(func.count()).select_from(model),
            reg,
            filters
        )

        count = await session.scalar(stmt)
        return count