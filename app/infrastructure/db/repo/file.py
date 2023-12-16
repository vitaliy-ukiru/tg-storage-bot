from typing import TypeVar, Sequence

from asyncpg import UniqueViolationError
from sqlalchemy import select, ColumnExpressionArgument, delete
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count

from app.core.domain.exceptions.file import FileAlreadyExists, FileNotFound, InvalidFilterError
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import File, FileId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.file import FilterField, FileRepository
from app.infrastructure.db import models
from .filters.file_filters import Registry

T = TypeVar("T")


def filter_convert(f: FilterField[T]) -> ColumnExpressionArgument[bool]:
    filter_func = Registry.get(f.name)
    if filter_func is None:
        raise InvalidFilterError(f.name)

    return filter_func(f.value)


class FileStorage(FileRepository):
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    async def save_file(self, file: File) -> FileId:
        async with self._pool() as session:
            db_file = models.File(
                remote_id=file.remote_file_id,
                user_id=file.user_id,
                type_id=file.type,
                title=file.title,
                created_at=file.created_at,
            )
            if file.category:
                db_file.category_id = file.category.id
            try:
                session.add(db_file)
                await session.commit()

            except UniqueViolationError:
                await session.rollback()
                raise FileAlreadyExists(file.remote_file_id)

            return FileId(db_file.id)

    async def get_file(self, file_id: FileId) -> File:
        async with self._pool() as session:
            db_file: models.File | None = await session.get(
                models.File,
                file_id,
                options=[joinedload(models.File.category)]
            )
            if db_file is None:
                raise FileNotFound(file_id)
            return db_file.to_domain()

    async def find_files(self, filters: Sequence[FilterField]) -> list[File]:
        async with self._pool() as session:
            sql = select(models.File)
            for f in filters:
                sql = sql.where(filter_convert(f))

            sql = sql.options(joinedload(models.File.category))
            res = await session.execute(sql)
            files = res.scalars()
            return [
                file.to_domain()

                for file in files
            ]

    async def update_file(self, file: File):
        async with self._pool() as session:
            model: models.File | None = await session.get(models.File, int(file.id))
            if model is None:
                raise FileNotFound(file.id)

            if file.category is not None and file.category.id != model.category_id:
                model.category_id = file.category.id

            if file.type != model.type_id:
                model.type_id = file.type

            if file.remote_file_id != model.remote_id:
                model.remote_id = str(file.remote_file_id)

            if file.title != model.title:
                model.title = file.title

            await session.commit()

    async def delete_file(self, file_id: FileId):
        async with self._pool() as session:
            sql = delete(models.File).where(models.File.id == int(file_id))
            await session.execute(sql)
            await session.commit()

    async def get_categories_usage_rate(self, user_id: UserId) -> dict[CategoryId, int]:
        async with self._pool() as session:
            sql = (select(models.File.category_id, count().label("rate")).
                   where(models.File.user_id == user_id).
                   group_by(models.File.category_id))
            res = await session.execute(sql)

            return {
                CategoryId(category_id): rate
                for category_id, rate in res.all()
            }
