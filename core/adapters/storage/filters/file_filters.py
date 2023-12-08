__all__ = (
    'Registry',
    'Filter'
)

from abc import abstractmethod
from typing import Protocol, TypeVar, Sequence

from sqlalchemy import ColumnExpressionArgument

from core.adapters.storage.database import File as FileModel
from core.domain.models.category import CategoryId, Category
from core.domain.models.file import FileType
from core.domain.models.user import UserId, User

T = TypeVar('T')


# FilterFunc = Callable[[T], ColumnExpressionArgument[bool]]
class Filter(Protocol[T]):
    @abstractmethod
    def __call__(self, v: T) -> ColumnExpressionArgument[bool]:
        raise NotImplementedError


_REGISTRY: dict[str, 'Filter'] = {}


class Registry:
    @classmethod
    def get(cls, name: str) -> Filter | None:
        return _REGISTRY.get(name)

    @classmethod
    def names(cls) -> tuple[str]:
        return tuple(_REGISTRY.keys())

    @classmethod
    def register(cls, name: str):
        def wrapper(func: Filter):
            _REGISTRY[name] = func
            return func

        return wrapper


@Registry.register("file_type")
def _file_type(value: FileType) -> ColumnExpressionArgument[bool]:
    return FileModel.type_id == value

@Registry.register("file_types")
def _file_types(value: Sequence[FileType]) -> ColumnExpressionArgument[bool]:
    return FileModel.type_id.in_(value)

@Registry.register("user_id")
def _user(value: UserId | int | User):
    if isinstance(value, User):
        value = value.id

    return FileModel.user_id == value


@Registry.register("category_id")
def _category(value: int | CategoryId | Category) -> ColumnExpressionArgument[bool]:
    if isinstance(value, Category):
        value = value.id
    return FileModel.category_id == value


@Registry.register("title_match")
def _title(value: str) -> ColumnExpressionArgument[bool]:
    return FileModel.title.icontains(value)
