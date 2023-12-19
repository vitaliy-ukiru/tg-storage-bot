from sqlalchemy import ColumnExpressionArgument

from app.core.domain.models.user import UserId
from .container import Container
from ...models import Category

categories = Container()

@categories("user_id")
def _user(value: UserId | int) -> ColumnExpressionArgument[bool]:
    return Category.user_id == value


@categories("title_match")
def _title(title: str) -> ColumnExpressionArgument[bool]:
    return Category.title.icontains(title)


@categories("favorites")
def _favorites(val: bool) -> ColumnExpressionArgument[bool]:
    return Category.is_favorite == val
