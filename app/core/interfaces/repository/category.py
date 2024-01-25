__all__ = (
    'CategoryRepoSaver',
    'CategoryRepoFinder',
    'CategoryRepoGetter',
    'CategoryRepoUpdater',
    'CategoryRepoUsageRater',
)

from abc import abstractmethod
from typing import Protocol, Optional, Sequence

from app.core.domain.dto.common import Pagination
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.common import FilterField


class CategoryRepoSaver(Protocol):
    @abstractmethod
    async def save_category(self, c: Category) -> CategoryId:
        raise NotImplementedError

class CategoryRepoGetter(Protocol):
    @abstractmethod
    async def get_category(self, category_id: CategoryId) -> Optional[Category]:
        raise NotImplementedError

class CategoryRepoUpdater(Protocol):
    @abstractmethod
    async def update_category(self, category: Category):
        raise NotImplementedError

class CategoryRepoFinder(Protocol):
    @abstractmethod
    async def find_categories(self, filters: Sequence[FilterField],
                              paginate: Optional[Pagination] = None) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def get_category_count(self, filters: Sequence[FilterField]) -> int:
        raise NotImplementedError

class CategoryRepoUsageRater(Protocol):
    @abstractmethod
    async def get_categories_usage(self, user_id: UserId) -> dict[CategoryId, int]:
        raise NotImplementedError
