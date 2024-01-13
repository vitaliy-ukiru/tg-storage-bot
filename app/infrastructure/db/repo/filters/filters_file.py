from typing import Sequence

from sqlalchemy import ColumnExpressionArgument

from app.core.domain.models.category import CategoryId, Category
from app.core.domain.models.file import FileCategory
from app.core.domain.models.user import UserId
from app.infrastructure.db.models import File as FileModel
from .container import Container

files = Container()


@files("file_categories")
def _file_categories(value: Sequence[FileCategory]) -> ColumnExpressionArgument[bool]:
    return FileModel.file_type.in_(value)


@files("user_id")
def _user(value: UserId | int):
    return FileModel.user_id == value


@files("category_id")
def _category(value: int | CategoryId | Category) -> ColumnExpressionArgument[bool]:
    if isinstance(value, Category):
        value = value.id
    return FileModel.category_id == value


@files("title_match")
def _title(value: str) -> ColumnExpressionArgument[bool]:
    return FileModel.title.icontains(value)
