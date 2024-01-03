import abc
from enum import Enum, auto

from aiogram_dialog import DialogManager

from app.core.common.filters.category import CategoryFilters
from app.core.domain.models.category import Category
from app.core.domain.models.user import User
from app.core.interfaces.usecase import CategoryUsecase


class CategoryFinder(abc.ABC):
    manager: DialogManager
    user: User
    category_service: CategoryUsecase

    def __init__(self, manager: DialogManager, user: User, category_service: CategoryUsecase):
        self.manager = manager
        self.user = user
        self.category_service = category_service

    @abc.abstractmethod
    async def find_categories(self) -> list[Category]:
        raise NotImplementedError


class PopularCategoriesFinder(CategoryFinder):
    async def find_categories(self) -> list[Category]:
        return await self.category_service.find_popular(self.user.id)


class FavoriteCategoriesFinder(CategoryFinder):
    async def find_categories(self) -> list[Category]:
        return await self.category_service.find_categories(
            CategoryFilters.user_id(self.user.id),
            CategoryFilters.favorites(True)
        )


class TitleCategoriesFinder(CategoryFinder):
    def __init__(self, manager: DialogManager, user: User, category_service: CategoryUsecase,
                 title: str):
        self._title = title

        super().__init__(manager, user, category_service)

    async def find_categories(self) -> list[Category]:
        return await self.category_service.find_categories(
            CategoryFilters.user_id(self.user.id),
            CategoryFilters.title_match(self._title)
        )


class FindMode(Enum):
    popular = auto()
    favorite = auto()
    title = auto()
