import abc
from typing import Protocol, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.sql.functions import count

from core.domain.models.category import Category, CategoryId
from core.domain.models.user import UserId

from .database import Category as CategoryModel, File as FileModel
from core.domain.services.category import CategoryRepository


class CategoryGateway(CategoryRepository):
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

    async def find_top_5_popular(self, user_id: UserId) -> list[Category]:
        sql = (select(CategoryModel).
               join(FileModel,
                    FileModel.category_id == CategoryModel.id and
                    CategoryModel.user_id == FileModel.user_id
                    ).
               where(CategoryModel.user_id == user_id).
               group_by(CategoryModel.id).
               order_by(count().desc()).
               limit(5))

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
