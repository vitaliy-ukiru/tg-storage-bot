from abc import abstractmethod
from typing import Protocol, TypeVar

from sqlalchemy import ColumnExpressionArgument

T = TypeVar('T')


class Filter(Protocol[T]):
    @abstractmethod
    def __call__(self, v: T) -> ColumnExpressionArgument[bool]:
        raise NotImplementedError



