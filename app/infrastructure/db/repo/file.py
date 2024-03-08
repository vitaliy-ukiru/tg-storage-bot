__all__ = (
    'FileStorageGateway',
    'FileCategoryUsageRater'
)

from typing import Sequence, Optional

from asyncpg import UniqueViolationError
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count

from app.core.domain.dto.common import Pagination
from app.core.domain.exceptions.file import FileAlreadyExists, FileNotFound
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import File, FileId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.category import CategoryRepoUsageRater
from app.core.interfaces.repository.common import FilterField
from app.core.interfaces.repository.file import (
    FileRepoSaver, FileRepoGetter, FileRepoFinder, FileRepoUpdater, FileRepoDeleter
)
from app.infrastructure.db import models
from ._base import BaseRepository
from .filters import Registry
from .utils import apply_pagination, apply_filters


class FileStorageGateway(
    FileRepoSaver,
    FileRepoGetter,
    FileRepoFinder,
    FileRepoUpdater,
    FileRepoDeleter,
    BaseRepository
):
    async def save_file(self, file: File) -> FileId:
        async with self._pool() as session:
            db_file = models.File(
                unique_id=file.remote_unique_id,
                remote_id=file.remote_file_id,
                user_id=file.user_id,
                file_type=file.type.category,
                mime_type=file.type.mime,
                title=file.title,
                created_at=file.created_at,
            )
            if file.category:
                db_file.category_id = file.category.id
            try:
                session.add(db_file)
                await session.commit()

            except (UniqueViolationError, IntegrityError):
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

    async def find_files(self,
                         filters: Sequence[FilterField],
                         paginate: Optional[Pagination] = None) -> list[File]:
        async with self._pool() as session:
            sql = apply_pagination(
                apply_filters(select(models.File), Registry.files, filters),
                paginate
            ).order_by(models.File.id)
            sql = sql.options(joinedload(models.File.category))
            res = await session.execute(sql)
            files = res.scalars()
            return [
                file.to_domain()

                for file in files
            ]

    async def get_files_count(self, filters: Sequence[FilterField]) -> int:
        async with self._pool() as session:
            return await self._get_count(
                session,
                models.File,
                Registry.files,
                filters
            )

    async def update_file(self, file: File):
        async with self._pool() as session:
            model: models.File | None = await session.get(models.File, int(file.id))
            if model is None:
                raise FileNotFound(file.id)

            if file.category is not None and file.category.id != model.category_id:
                model.category_id = file.category.id

            file_type = file.type
            if file_type.category != model.file_type:
                model.file_type = file_type.category

            if file_type.mime != model.mime_type:
                model.mime_type = file_type.mime

            if file.remote_file_id != model.remote_id:
                model.remote_id = str(file.remote_file_id)

            if file.remote_unique_id != model.unique_id:
                model.unique_id = file.remote_unique_id

            if file.title != model.title:
                model.title = file.title

            await session.commit()

    async def delete_file(self, file_id: FileId):
        async with self._pool() as session:
            sql = delete(models.File).where(models.File.id == int(file_id))
            await session.execute(sql)
            await session.commit()


class FileCategoryUsageRater(
    CategoryRepoUsageRater,
    BaseRepository,
):
    async def get_categories_usage(self, user_id: UserId) -> dict[CategoryId, int]:
        async with self._pool() as session:
            rate = count().label("rate")
            sql = (
                select(models.File.category_id, rate).
                where(models.File.user_id == user_id).
                group_by(models.File.category_id)
            )
            res = await session.execute(sql)
            return {
                CategoryId(category_id): rate
                for category_id, rate in res.all()
            }
