from abc import abstractmethod
from typing import Optional, Protocol

from app.core.domain.dto.common import Pagination
from app.core.domain.models.category import CategoryId
from app.core.domain.models.user import UserId
from app.core.domain.services.category import CategoryRater


class CategoryUsageRepo(Protocol):
    @abstractmethod
    async def get_categories_usage(self, user_id: UserId) -> list[tuple[CategoryId, int]]:
        raise NotImplementedError


class CategoryRaterAdapter(CategoryRater):
    _repo: CategoryUsageRepo

    def __init__(self, repo: CategoryUsageRepo):
        self._repo = repo

    async def get_usage_rate(self, user_id: UserId) -> dict[CategoryId, int]:
        rates = await self._repo.get_categories_usage(user_id)
        return {
            category_id: count
            for category_id, count in rates
            if category_id is not None
        }
