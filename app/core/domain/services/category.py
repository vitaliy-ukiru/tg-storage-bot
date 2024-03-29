from dataclasses import asdict
from datetime import datetime
from typing import Optional

from app.common.helpers import is_category_marker_valid
from app.core.domain.dto.category import CreateCategoryDTO, CategoriesFindDTO, UpdateCategoryDTO
from app.core.domain.dto.common import Pagination
from app.core.domain.exceptions.category import CategoryNotFound, InvalidCategoryMarker, \
    CategoryAccessDenied
from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId
from app.core.domain.services.internal import convert_to_filter_fields
from app.core.interfaces.repository.category import (
    CategoryRepoSaver, CategoryRepoGetter, CategoryRepoFinder, CategoryRepoUpdater,
    CategoryRepoUsageRater
)
from app.core.interfaces.usecase import CategoryUsecase

UNDEFINED_CATEGORY_ID = CategoryId(0)


def _ensure_owner(category: Category, user_id: UserId):
    if category.user_id != user_id:
        raise CategoryAccessDenied(category.id, user_id)


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
        if dto.marker:
            ensure_valid_marker(dto.marker, UNDEFINED_CATEGORY_ID)

        c = Category(
            id=UNDEFINED_CATEGORY_ID,
            user_id=UserId(dto.user_id),
            title=dto.title,
            description=dto.desc,
            created_at=datetime.now(),
            marker=dto.marker,
        )

        c.id = await self._saver.save_category(c)
        return c

    async def get_category(self, category_id: CategoryId, user_id: UserId) -> Category:
        c = await self._getter.get_category(category_id)
        if c is None:
            raise CategoryNotFound(category_id)

        _ensure_owner(c, user_id)
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

    async def update_category(self, dto: UpdateCategoryDTO, user_id: UserId) -> Category:
        category = await self.get_category(dto.category_id, user_id)
        _ensure_owner(category, user_id)
        if dto.title is not None:
            category.title = dto.title

        if dto.desc is not None:
            category.description = dto.desc

        if dto.delete_desc:
            category.description = None

        if dto.favorite is not None:
            category.is_favorite = dto.favorite

        if dto.marker is not None and not dto.delete_marker:
            ensure_valid_marker(dto.marker, category.id)
            category.marker = dto.marker

        if dto.delete_marker:
            category.marker = None

        await self._updater.update_category(category)
        return category


def ensure_valid_marker(marker: str, category_id: CategoryId) -> None:
    if not is_category_marker_valid(marker):
        raise InvalidCategoryMarker(category_id)
