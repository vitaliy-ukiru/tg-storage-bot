__all__ = (
    'CategoryRepository',
)
import abc
from typing import Protocol, Optional

from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId


class CategoryRepository(Protocol):
    @abc.abstractmethod
    async def save_category(self, c: Category) -> CategoryId:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_category(self, category_id: CategoryId) -> Optional[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_user_categories(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_favorites_categories(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        raise NotImplementedError
