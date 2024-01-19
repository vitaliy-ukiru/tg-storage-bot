from typing import Sequence, Optional

from sqlalchemy import Select

from app.core.domain.dto.common import Pagination, OrderFields, Ordering
from app.core.interfaces.repository.common import FilterField
from .filters.container import Container
from ..models import File, Category


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


_COLUMNS = {
    OrderFields.file_id: File.id,
    OrderFields.file_title: File.title,
    OrderFields.file_type: File.file_type,
    OrderFields.file_user: File.user_id,
    OrderFields.file_created_at: File.created_at,
    OrderFields.file_category: File.category_id,

    OrderFields.category_id: Category.id,
    OrderFields.category_user: Category.user_id,
    OrderFields.category_title: Category.title,
    OrderFields.category_description: Category.description,
    OrderFields.category_is_favorite: Category.is_favorite,
    OrderFields.category_created_at: Category.created_at,
}


def get_order_column(ordering: Ordering):
    col = _COLUMNS[ordering.field]
    if ordering.reverse:
        col = col.desc()

    return col
