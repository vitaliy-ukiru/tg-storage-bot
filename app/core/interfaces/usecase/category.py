__all__ = (
    'CategoryUsecase',
)
import abc
from typing import Protocol

from app.core.domain.dto.category import CreateCategoryDTO
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId


class CategoryUsecase(Protocol):
    @abc.abstractmethod
    async def save_category(self, dto: CreateCategoryDTO) -> Category:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_category(self, category_id: CategoryId) -> Category:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_popular(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_favorites(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        raise NotImplementedError
