from typing import Sequence, Optional

from sqlalchemy import Select

from app.core.domain.dto.common import Pagination
from app.core.interfaces.repository.common import FilterField
from .filters.container import Container

def apply_pagination(stmt: Select, p: Optional[Pagination]) -> Select:
    if p is None:
        return stmt
    if p.limit is not None:
        stmt = stmt.limit(p.limit)
    if p.offset is not None:
        stmt = stmt.offset(p.offset)

    return stmt


def apply_filters(stmt: Select, reg: Container, filters: Sequence[FilterField]) -> Select:
    for f in filters:
        stmt = stmt.where(reg.convert(f))
    return stmt
