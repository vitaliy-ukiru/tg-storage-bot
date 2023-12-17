from sqlalchemy import ColumnExpressionArgument

from app.core.domain.models.user import UserId
from .registry import Registry
from ...models import Category

_categories = Registry.categories


@_categories("user_id")
def _user(value: UserId | int) -> ColumnExpressionArgument[bool]:
    return Category.user_id == value


@_categories("title_match")
def _title(title: str) -> ColumnExpressionArgument[bool]:
    return Category.title.icontains(title)


@_categories("favorites")
def _favorites(val: bool) -> ColumnExpressionArgument[bool]:
    return Category.is_favorite == val
