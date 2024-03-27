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
from app.core.domain.models.auth import Issuer
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId


class CategorySaver(Protocol):
    @abc.abstractmethod
    async def save_category(self, dto: CreateCategoryDTO, issuer: Issuer) -> Category:
        raise NotImplementedError


class CategoryGetter(Protocol):
    @abc.abstractmethod
    async def get_category(self, category_id: CategoryId, issuer: Issuer) -> Category:
        raise NotImplementedError


class CategoryUpdater(Protocol):
    @abc.abstractmethod
    async def update_category(self, dto: UpdateCategoryDTO, issuer: Issuer) -> Category:
        raise NotImplementedError


class CategoryFinder(Protocol):
    @abc.abstractmethod
    async def find_popular(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_categories(
        self,
        dto: CategoriesFindDTO,
        paginate: Optional[Pagination] = None
    ) -> list[Category]:
        raise NotImplementedError


class CategoryUsecase(
    CategorySaver,
    CategoryGetter,
    CategoryFinder,
    CategoryUpdater,
):
    pass
