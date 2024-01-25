__all__ = (
    'CategorySaver',
    'CategoryFinder',
    'CategoryGetter',
    'CategoryUpdater',
    'CategoryUsageRater',
)

from abc import abstractmethod
from typing import Protocol, Optional, Sequence

from app.core.domain.dto.common import Pagination
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.common import FilterField


class CategorySaver(Protocol):
    @abstractmethod
    async def save_category(self, c: Category) -> CategoryId:
        raise NotImplementedError

class CategoryGetter(Protocol):
    @abstractmethod
    async def get_category(self, category_id: CategoryId) -> Optional[Category]:
        raise NotImplementedError

class CategoryUpdater(Protocol):
    @abstractmethod
    async def update_category(self, category: Category):
        raise NotImplementedError

class CategoryFinder(Protocol):
    @abstractmethod
    async def find_categories(self, filters: Sequence[FilterField],
                              paginate: Optional[Pagination] = None) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def get_category_count(self, filters: Sequence[FilterField]) -> int:
        raise NotImplementedError

class CategoryUsageRater(Protocol):
    @abstractmethod
    async def get_categories_usage(self, user_id: UserId) -> dict[CategoryId, int]:
        raise NotImplementedError
