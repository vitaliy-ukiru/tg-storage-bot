__all__ = (
    'Registry',
    'FileTypeFilter',
    'UserFilter',
    'CategoryFilter',
    'TitleMatchFilter',
)

from abc import ABC, abstractmethod
from typing import Tuple, Any, Protocol, TypeVar

from sqlalchemy import ColumnExpressionArgument

from core.adapters.storage.database import File as FileModel
from core.domain.models.category import CategoryId, Category
from core.domain.models.file import FileType
from core.domain.models.user import UserId, User

_REGISTRY: dict[str, type] = {}

T = TypeVar('T')


class Filter(Protocol[T]):
    @property
    @abstractmethod
    def clause(self) -> ColumnExpressionArgument[bool]:
        raise NotImplementedError


class BaseFilter(Filter[T], ABC):
    def __init__(self, value: T):
        self._value = value

    def __init_subclass__(cls, *, name: str = None, **kwargs):
        if name is None:
            raise ValueError("name is required")
        cls.__filter_name__ = name
        _REGISTRY[name] = cls
        super().__init_subclass__(**kwargs)

    @property
    def name(self) -> str:
        return self.__filter_name__


class Registry:
    @classmethod
    def get(cls, name: str) -> type[BaseFilter] | None:
        return _REGISTRY.get(name)

    @classmethod
    def names(cls) -> tuple[str]:
        return tuple(_REGISTRY.keys())


class FileTypeFilter(BaseFilter[FileType], name="file_type"):

    @property
    def clause(self) -> ColumnExpressionArgument[bool]:
        return FileModel.type_id == self._value


class UserFilter(BaseFilter[UserId | int], name="user_id"):
    def __init__(self, value: UserId | int | User):
        if isinstance(value, User):
            value = value.id

        super().__init__(value)

    @property
    def clause(self) -> ColumnExpressionArgument[bool]:
        return FileModel.user_id == self._value


class CategoryFilter(BaseFilter[int | CategoryId], name="category_id"):

    def __init__(self, value: int | CategoryId | Category):
        if isinstance(value, Category):
            value = value.id

        super().__init__(value)

    @property
    def clause(self) -> ColumnExpressionArgument[bool]:
        return FileModel.category_id == self._value


class TitleMatchFilter(BaseFilter[str], name="title_match"):
    @property
    def clause(self) -> ColumnExpressionArgument[bool]:
        return FileModel.title.icontains(self._value)
