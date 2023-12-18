__all__ = (
    'CategoryRepository',
)
import abc
from typing import Protocol, Optional, Sequence

from app.core.domain.models.category import Category, CategoryId
from app.core.interfaces.repository.file import FilterField


class CategoryRepository(Protocol):
    @abc.abstractmethod
    async def save_category(self, c: Category) -> CategoryId:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_category(self, category_id: CategoryId) -> Optional[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_category(self, category: Category):
        raise NotImplementedError

    @abc.abstractmethod
    async def find_categories(self, filters: Sequence[FilterField]) -> list[Category]:
        raise NotImplementedError
