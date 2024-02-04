from dataclasses import asdict
from datetime import datetime
from typing import Optional

from app.core.domain.dto.category import CreateCategoryDTO, CategoriesFindDTO, UpdateCategoryDTO
from app.core.domain.dto.common import Pagination
from app.core.domain.exceptions.category import CategoryNotFound
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId
from app.core.domain.services.internal import convert_to_filter_fields
from app.core.interfaces.repository.category import (
    CategoryRepoSaver, CategoryRepoGetter, CategoryRepoFinder, CategoryRepoUpdater,
    CategoryRepoUsageRater
)
from app.core.interfaces.usecase.category import CategoryUsecase

UNDEFINED_CATEGORY_ID = CategoryId(0)


class CategoryService(CategoryUsecase):
    _saver: CategoryRepoSaver
    _getter: CategoryRepoGetter
    _finder: CategoryRepoFinder
    _updater: CategoryRepoUpdater
    _rater: CategoryRepoUsageRater

    def __init__(
        self,
        saver: CategoryRepoSaver,
        getter: CategoryRepoGetter,
        finder: CategoryRepoFinder,
        updater: CategoryRepoUpdater,
        rater: CategoryRepoUsageRater,
    ):

        self._saver = saver
        self._getter = getter
        self._finder = finder
        self._updater = updater
        self._rater = rater

    async def save_category(self, dto: CreateCategoryDTO) -> Category:
        c = Category(
            id=UNDEFINED_CATEGORY_ID,
            user_id=UserId(dto.user_id),
            title=dto.title,
            description=dto.desc,
            created_at=datetime.now(),
        )

        c.id = await self._saver.save_category(c)
        return c

    async def get_category(self, category_id: CategoryId) -> Category:
        c = await self._getter.get_category(category_id)
        if c is None:
            raise CategoryNotFound(category_id)

        return c

    async def find_categories(
        self,
        dto: CategoriesFindDTO,
        paginate: Optional[Pagination] = None
    ) -> list[Category]:
        filters = convert_to_filter_fields(asdict(dto))
        categories = await self._finder.find_categories(filters, paginate)
        return categories

    async def find_popular(self, user_id: UserId) -> list[Category]:
        categories = await self.find_categories(CategoriesFindDTO(
            user_id=user_id,
        ))
        if len(categories) == 0:
            return categories

        categories_rates = await self._rater.get_categories_usage(user_id)
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

        await self._updater.update_category(category)
        return category
