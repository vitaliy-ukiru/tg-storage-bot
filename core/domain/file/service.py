from asyncpg import UniqueViolationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import noload, lazyload, joinedload

from core.domain.file import File, NamedCategory
from core import database as db
from core.domain.file.dto import CreateFileDTO
from core.domain.file.exceptions import FileAlreadyExists


class FileService:
    _pool: async_sessionmaker

    async def create_file(self, file_dto: CreateFileDTO) -> File:
        async with self._pool() as session:
            db_file = db.File(
                remote_id=file_dto.remote_id,
                user_id=file_dto.user_id,
                file_type=file_dto.file_type,
                category_id=file_dto.category_id,
                title=file_dto.title,
            )
            try:
                session.add(db_file)
                await session.commit()

            except UniqueViolationError:
                await session.rollback()
                raise FileAlreadyExists(file_dto.remote_id)

            file = File(
                file_id=db_file.id,
                file_type=db_file.type_id,
                remote_file_id=db_file.remote_id,
                user_id=db_file.user_id,
                created_at=db_file.created_at,
                title=db_file.title,
            )

            # TODO: improve this code
            if db_file.category_id is not None:
                sql = select(db.Category).where(db.Category.id == db_file.category_id).options(noload())
                res = await session.execute(sql)
                category = res.scalar()
                file.category = NamedCategory(category.id, category.title)

            return file

    async def get_file_by_id(self, file_id: int) -> File:
        async with self._pool() as session:
            sql = select(db.File).where(db.File.id == file_id).options(
                joinedload(db.File.category),
                joinedload(db.File.user)
            )
            res = await session.execute(sql)
            db_file = res.scalar()

            file = File(
                file_id=db_file.id,
                file_type=db_file.type_id,
                remote_file_id=db_file.remote_id,
                user_id=db_file.user_id,
                created_at=db_file.created_at,
                title=db_file.title,
            )

            # TODO: improve this code
            if db_file.category_id is not None:
                category = db_file.category
                file.category = NamedCategory(category.id, category.title)

            return file
