import abc
from datetime import datetime
from typing import Protocol, Optional

from core.domain.dto.category import CreateCategoryDTO
from core.domain.exceptions.category import CategoryNotFound
from core.domain.models.category import Category, CategoryId
from core.domain.models.user import UserId


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
    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        raise NotImplementedError


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
    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        raise NotImplementedError


class CategoryRate(Protocol):
    @abc.abstractmethod
    async def get_categories_usage_rate(self, user_id: UserId) -> dict[CategoryId, int]:
        raise NotImplementedError


UNDEFINED_CATEGORY_ID = CategoryId(0)


class CategoryService(CategoryUsecase):
    _repo: CategoryRepository
    _counter: CategoryRate

    def __init__(self, repo: CategoryRepository, counter: CategoryRate):
        self._repo = repo
        self._counter = counter

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

    async def find_popular(self, user_id: UserId) -> list[Category]:
        # return await self._repo.find_top_5_popular(user_id)
        categories = await self._repo.find_user_categories(user_id)
        if len(categories) == 0:
            return categories

        categories_rates = await self._counter.get_categories_usage_rate(user_id)
        if len(categories_rates) == 0:
            return categories

        categories.sort(
            key=lambda c: categories_rates.get(c.id, 0),
            reverse=True
        )
        return categories

    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        return await self._repo.find_by_title(user_id, title_mask)
