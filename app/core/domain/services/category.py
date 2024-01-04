import abc
from dataclasses import asdict
from datetime import datetime
from typing import Protocol, Optional

from app.core.domain.dto.category import CreateCategoryDTO, CategoriesFindDTO, UpdateCategoryDTO
from app.core.domain.dto.common import Pagination
from app.core.domain.exceptions.category import CategoryNotFound
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.category import CategoryRepository
from app.core.interfaces.repository.common import FilterField
from app.core.interfaces.usecase.category import CategoryUsecase
from app.core.domain.services.internal.filter_merger import FilterMerger
from app.core.common.filters.category import CategoryFilters


class CategoryRater(Protocol):
    @abc.abstractmethod
    async def get_usage_rate(self, user_id: UserId) -> dict[CategoryId, int]:
        raise NotImplementedError


UNDEFINED_CATEGORY_ID = CategoryId(0)


class CategoryService(CategoryUsecase):
    _repo: CategoryRepository
    _rater: CategoryRater

    def __init__(self, repo: CategoryRepository, rater: CategoryRater):
        self._repo = repo
        self._rater = rater

    async def save_category(self, dto: CreateCategoryDTO) -> Category:
        c = Category(
            id=UNDEFINED_CATEGORY_ID,
            user_id=UserId(dto.user_id),
            title=dto.title,
            description=dto.desc,
            created_at=datetime.now(),
        )

        c.id = await self._repo.save_category(c)
        return c

    async def get_category(self, category_id: CategoryId) -> Category:
        c = await self._repo.get_category(category_id)
        if c is None:
            raise CategoryNotFound(category_id)

        return c

    async def find_categories(self,
                              *filters: FilterField,
                              dto: CategoriesFindDTO = None,
                              paginate: Optional[Pagination] = None) -> list[Category]:
        dto_items = asdict(dto) if dto else None

        filters = FilterMerger.merge(dto_items, filters)
        FilterMerger.ensure_have_user_id(filters)

        categories = await self._repo.find_categories(filters, paginate)
        return categories

    async def find_popular(self, user_id: UserId) -> list[Category]:
        categories = await self.find_categories(CategoryFilters.user_id(user_id))
        if len(categories) == 0:
            return categories

        categories_rates = await self._rater.get_usage_rate(user_id)
        if len(categories_rates) == 0:
            return categories

        categories.sort(
            key=lambda c: categories_rates.get(c.id, 0),
            reverse=True
        )
        return categories

    async def update_category(self, dto: UpdateCategoryDTO) -> Category:
        category = await self.get_category(dto.category_id)
        if dto.title is not None:
            category.title = dto.title

        if dto.desc is not None:
            category.description = dto.desc

        if dto.delete_desc:
            category.description = None

        if dto.favorite is not None:
            category.is_favorite = dto.favorite

        await self._repo.update_category(category)
        return category
