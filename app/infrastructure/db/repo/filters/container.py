from typing import TypeVar

from sqlalchemy import ColumnExpressionArgument

from app.core.domain.exceptions.base import InvalidFilterError
from app.core.interfaces.repository.file import FilterField
from .base import Filter

T = TypeVar('T')

class Container:
    _reg: dict[str, Filter]

    def __init__(self):
        self._reg = {}

    def __call__(self, name: str):
        return self.register(name)

    def get(self, name: str) -> Filter | None:
        return self._reg.get(name)

    def names(self) -> tuple[str]:
        return tuple(self._reg.keys())

    def register(self, name: str):
        def wrapper(func: Filter):
            self._reg[name] = func
            return func

        return wrapper

    def convert(self, f: FilterField[T]) -> ColumnExpressionArgument[bool]:
        filter_func = self.get(f.name)
        if filter_func is None:
            raise InvalidFilterError(f.name)

        return filter_func(f.value)
