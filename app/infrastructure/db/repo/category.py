from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.domain.models.category import Category, CategoryId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.category import CategoryRepository
from app.infrastructure.db import Category as CategoryModel


class CategoryStorage(CategoryRepository):
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    async def save_category(self, c: Category) -> CategoryId:
        async with self._pool() as session:
            db_category = CategoryModel(
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
            category: Optional[CategoryModel] = await session.get(CategoryModel, int(category_id))
            return category.to_domain() if category else None

    async def find_user_categories(self, user_id: UserId) -> list[Category]:
        sql = select(CategoryModel).where(CategoryModel.user_id == user_id)
        async with self._pool() as session:
            res = await session.execute(sql)
            categories = res.scalars()
            return [
                c.to_domain()
                for c in categories
            ]

    async def find_by_title(self, user_id: UserId, title_mask: str) -> list[Category]:
        sql = (select(CategoryModel).where(
            CategoryModel.user_id == user_id,
            CategoryModel.title.icontains(title_mask),
        ))

        async with self._pool() as session:
            res = await session.execute(sql)
            categories = res.scalars()
            return [
                c.to_domain()
                for c in categories
            ]
