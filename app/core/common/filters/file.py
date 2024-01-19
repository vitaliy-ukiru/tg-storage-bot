from typing import Sequence

from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import FileCategory
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.common import FilterField


class FileFilters:
    @classmethod
    def file_categories(cls, *value: FileCategory) -> FilterField[Sequence[FileCategory]]:
        return FilterField("file_types", value)

    @classmethod
    def user_id(cls, value: UserId | int) -> FilterField[UserId | int]:
        return FilterField("user_id", value)

    @classmethod
    def category_id(cls, value: CategoryId | int) -> FilterField[CategoryId | int]:
        return FilterField("category_id", value)

    @classmethod
    def title_match(cls, value: str) -> FilterField[str]:
        return FilterField("title_match", value)
