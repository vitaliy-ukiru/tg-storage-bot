from typing import Sequence

from sqlalchemy import ColumnExpressionArgument

from app.core.domain.models.category import CategoryId, Category
from app.core.domain.models.file import FileType
from app.core.domain.models.user import UserId
from app.infrastructure.db.models import File as FileModel
from .container import Container

files = Container()


@files("file_type")
def _file_type(value: FileType):
    return FileModel.type_id == value


@files("file_types")
def _file_types(value: Sequence[FileType]):
    return FileModel.type_id.in_(value)


@files("user_id")
def _user(value: UserId | int):
    return FileModel.user_id == value


@files("category_id")
def _category(value: int | CategoryId | Category):
    if isinstance(value, Category):
        value = value.id
    return FileModel.category_id == value


@files("title_match")
def _title(value: str):
    return FileModel.title.icontains(value)
