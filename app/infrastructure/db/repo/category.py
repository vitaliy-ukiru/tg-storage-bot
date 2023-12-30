from typing import Optional, Sequence

from sqlalchemy import select

from app.core.domain.dto.common import Pagination
from app.core.domain.exceptions.category import CategoryNotFound
from app.core.domain.models.category import Category, CategoryId
from app.core.interfaces.repository.category import CategoryRepository
from app.core.interfaces.repository.common import FilterField
from app.infrastructure.db import models
from app.infrastructure.db.repo.filters import Registry
from ._base import BaseRepository


class CategoryStorage(BaseRepository, CategoryRepository):

    async def save_category(self, c: Category) -> CategoryId:
        async with self._pool() as session:
            db_category = models.Category(
                user_id=int(c.user_id),
                title=c.title,
                created_at=c.created_at,
                description=c.description,
            )
            session.add(db_category)
            await session.commit()
            return CategoryId(db_category.id)

    async def get_category(self, category_id: CategoryId) -> Optional[Category]:
        async with self._pool() as session:
            category: Optional[models.Category] = await session.get(
                models.Category,
                int(category_id)
            )
            return category.to_domain() if category else None

    async def find_categories(self,
                              filters: Sequence[FilterField],
                              paginate: Optional[Pagination] = None) -> list[Category]:
        async with self._pool() as session:
            sql = self.apply_pagination(
                self.apply_filters(select(models.Category), Registry.categories, filters),
                paginate
            ).order_by(models.Category.id)

            res = await session.execute(sql)
            categories = res.scalars()
            return [c.to_domain() for c in categories]

    async def update_category(self, category: Category):
        async with self._pool() as session:
            model: models.Category | None = await session.get(models.Category, int(category.id))
            if model is None:
                raise CategoryNotFound(category.id)

            if category.title != model.title:
                model.title = category.title

            if category.description != model.description:
                model.description = category.description

            if category.is_favorite != model.is_favorite:
                model.is_favorite = category.is_favorite

            await session.commit()
