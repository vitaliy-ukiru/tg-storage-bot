__all__ = (
    'CategoryUsecase',
    'CategorySaver',
    'CategoryGetter',
    'CategoryUpdater',
    'CategoryFinder',
)

import abc
from typing import Protocol, Optional

from app.core.domain.dto.category import CreateCategoryDTO, CategoriesFindDTO, UpdateCategoryDTO
from app.core.domain.dto.common import Pagination
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.common import FilterField


class CategorySaver(Protocol):
    @abc.abstractmethod
    async def save_category(self, dto: CreateCategoryDTO) -> Category:
        raise NotImplementedError


class CategoryGetter(Protocol):
    @abc.abstractmethod
    async def get_category(self, category_id: CategoryId) -> Category:
        raise NotImplementedError


class CategoryUpdater(Protocol):
    @abc.abstractmethod
    async def update_category(self, dto: UpdateCategoryDTO) -> Category:
        raise NotImplementedError


class CategoryFinder(Protocol):
    @abc.abstractmethod
    async def find_popular(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_categories(self,
                              *filters: FilterField,
                              dto: Optional[CategoriesFindDTO] = None,
                              paginate: Optional[Pagination] = None) -> list[Category]:
        raise NotImplementedError


class CategoryUsecase(
    CategorySaver,
    CategoryFinder,
    CategoryUpdater,
):
    pass
