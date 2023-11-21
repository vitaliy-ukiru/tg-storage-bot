import abc
from typing import cast

from asyncpg import UniqueViolationError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import noload, joinedload
from sqlalchemy.orm.interfaces import LoaderOption

from core import database as db
from .model import Category
from core.domain.file import File
from core.domain.file.dto import CreateFileDTO, ReloadFileDTO
from core.domain.file.exceptions import FileAlreadyExists, FileCategoryViolation, FileNotFound


class FileUseCase(abc.ABC):
    @abc.abstractmethod
    async def create_file(self, file_dto: CreateFileDTO) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_file_by_id(self, file_id: int) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_title(self, file_id: int, title: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def reload_file(self, file_id: int, reload_file: ReloadFileDTO):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_file(self, file_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def set_category(self, file_id: int, category: Category) -> File:
        raise NotImplementedError


class FileService(FileUseCase):
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    async def create_file(self, file_dto: CreateFileDTO) -> File:
        async with self._pool() as session:
            db_file = db.File(
                remote_id=file_dto.remote_id,
                user_id=file_dto.user_id,
                type_id=file_dto.file_type,
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
                file.category = category.to_domain()

            return file

    async def get_file_by_id(self, file_id: int) -> File:
        async with self._pool() as session:
            sql = select(db.File).where(db.File.id == file_id).options(
                joinedload(db.File.category),
                joinedload(db.File.user)
            )
            res = await session.execute(sql)
            db_file = res.scalar()
            return db_file.to_domain()

    async def update_title(self, file_id: int, title: str):
        async with self._pool() as session:
            sql = update(db.File).where(db.File.id == file_id).values(title=title)
            await session.execute(sql)
            await session.commit()

    async def reload_file(self, file_id: int, reload_file: ReloadFileDTO):
        async with self._pool() as session:
            db_file = await session.get(db.File, file_id)
            if db_file is None:
                raise FileNotFound(file_id)

            db_file = cast(db.File, db_file)

            new_title = reload_file.title
            if db_file.title == db_file.remote_id or db_file.title is None:
                db_file.title = new_title

            db_file.remote_id = reload_file.remote_id
            db_file.type_id = reload_file.file_type
            await session.merge(db_file)
            await session.commit()

        #     sql = update(db.File).where(db.File.id == file_id).values(**values)
        # values = reload_file.__dict__.copy()
        # if reload_file.title is None:
        #     values.pop("title")
        #
        #     await session.execute(sql)
        #     await session.commit()

    async def delete_file(self, file_id: int):
        async with self._pool() as session:
            await session.delete(db.File(id=file_id))
            await session.commit()

    async def set_category(self, file_id: int, category: Category) -> File:
        async with self._pool() as session:
            db_file = await session.get(db.File, file_id)
            if db_file is None:
                raise FileNotFound(str(file_id))

            db_file = cast(db.File, db_file)
            if db_file.user_id != category.user_id:
                raise FileCategoryViolation(db_file.remote_id, category)

            db_file.category_id = category.id
            # TODO: FIX: not load category
            db_file = await session.merge(db_file, load=True, options=[LoaderOption()])
            await session.commit()

            return db_file.to_domain()
