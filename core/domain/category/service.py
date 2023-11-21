import abc
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.sql.functions import count

from .dto import CreateCategoryDTO
from .models import Category
from core import database as db


class CategoryUseCase(abc.ABC):
    @abc.abstractmethod
    async def find_top_5_popular(self, user_id: int) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by_title(self, user_id: int, title_mask: str) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_category(self, new_category: CreateCategoryDTO) -> Category:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_category(self, category_id: int) -> Category:
        raise NotImplementedError


class CategoryService(CategoryUseCase):
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    async def find_top_5_popular(self, user_id: int) -> list[Category]:
        sql = (select(db.Category).
               join(db.File,
                    db.File.category_id == db.Category.id and db.Category.user_id == db.File.user_id).
               where(db.Category.user_id == user_id).
               group_by(db.Category.id).
               order_by(count().desc()).
               limit(5))

        async with self._pool() as session:
            res = await session.execute(sql)
            categories = res.scalars()
            return [
                c.to_domain()
                for c in categories
            ]

    async def find_by_title(self, user_id: int, title_mask: str) -> list[Category]:
        sql = (select(db.Category).where(
            db.Category.user_id == user_id,
            db.Category.title.match(title_mask),
        ))

        async with self._pool() as session:
            res = await session.execute(sql)
            categories = res.scalars()
            return [
                c.to_domain()
                for c in categories
            ]

    async def create_category(self, new_category: CreateCategoryDTO) -> Category:
        async with self._pool() as session:
            c = db.Category(
                user_id=new_category.user_id,
                title=new_category.title,
                description=new_category.desc,
            )
            session.add(c)
            await session.commit()
            return c.to_domain()

    async def get_category(self, category_id: int) -> Category:
        sql = select(db.Category).where(db.Category.id == category_id)

        async with self._pool() as session:
            res = await session.execute(sql)
            category = res.scalar()
            return category.to_domain()
