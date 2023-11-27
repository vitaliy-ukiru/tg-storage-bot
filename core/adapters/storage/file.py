import abc
from typing import Protocol, TypeVar, Sequence

from asyncpg import UniqueViolationError
from sqlalchemy import select, ColumnExpressionArgument
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

from core.domain.models.file import File, FileId
from core.domain.services.file import FileRepository, FilterField
from core.domain.exceptions.file import FileAlreadyExists, FileNotFound, InvalidFilterError

from .database.models import File as FileModel
from .filters.file_filters import Filter, Registry

T = TypeVar("T")

def filter_convert(f: FilterField) -> Filter[T]:
    filter_type = Registry.get(f.name)
    if filter_type is None:
        raise InvalidFilterError(f.name)

    return filter_type(f.value)

class FileGateway(FileRepository):
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    async def save_file(self, file: File) -> FileId:
        async with self._pool() as session:
            db_file = FileModel(
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
            db_file: FileModel | None = await session.get(FileModel, file_id,
                                                          options=[joinedload(FileModel.category)])
            if db_file is None:
                raise FileNotFound(file_id)
            return db_file.to_domain()

    async def find_files(self, filters: Sequence[FilterField]) -> list[File]:
        async with self._pool() as session:
            sql = select(FileModel)
            for f in filters:
                sql = sql.where(filter_convert(f).clause)

            sql = sql.options(joinedload(FileModel.category))
            res = await session.execute(sql)
            files = res.scalars()
            return [
                file.to_domain()

                for file in files
            ]

    async def update_file(self, file: File):
        async with self._pool() as session:
            model: FileModel | None = await session.get(FileModel, int(file.id))
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
            await session.delete(FileModel(id=int(file_id)))
            await session.commit()
