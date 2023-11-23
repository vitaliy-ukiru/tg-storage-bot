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
    async def find_top_5_popular(self, user_id: UserId) -> list[Category]:
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
    async def find_top_5_popular(self, user_id: UserId) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        raise NotImplementedError


UNDEFINED_CATEGORY_ID = CategoryId(0)


class CategoryService(CategoryUsecase):
    _repo: CategoryRepository

    def __init__(self, repo: CategoryRepository):
        self._repo = repo

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

    async def find_top_5_popular(self, user_id: UserId) -> list[Category]:
        return await self._repo.find_top_5_popular(user_id)

    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        return await self._repo.find_by_title(user_id, title_mask)
