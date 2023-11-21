import abc
from datetime import datetime
from typing import Protocol, cast

from asyncpg import UniqueViolationError
from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker
from core import database as db
from .exceptions import UserAlreadyExists, UserNotFound, UserDeleted
from .model import User


class UserUseCase(abc.ABC):

    @abc.abstractmethod
    async def create_user(self, user_id: int) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user(self, user_id: int, must_get: bool = False) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def restore_user(self, user: User | int):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_user(self, user: User | int):
        raise NotImplementedError


class UserService(UserUseCase):
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    async def create_user(self, user_id: int) -> User:
        db_user = db.User(id=user_id)
        async with self._pool() as session:
            try:
                session.add(db_user)
                await session.commit()
            except UniqueViolationError:
                await session.rollback()
                raise UserAlreadyExists(user_id)
            else:
                return db_user.to_domain()

    async def get_user(self, user_id: int, must_get: bool = False) -> User:
        async with self._pool() as session:
            db_user = await session.get(db.User, user_id)
            if db_user is None:
                if not must_get:
                    raise UserNotFound(user_id)

                db_user = db.User(id=user_id)
                session.add(db_user)
                await session.commit()

            db_user = cast(db.User, db_user)
            if db_user.deleted_at is not None:
                if not must_get:
                    raise UserDeleted(user_id)

                db_user.deleted_at = None
                await session.merge(db_user)
                await session.commit()

            return db_user.to_domain()

    async def restore_user(self, user: User | int):
        user_id: int = user
        if isinstance(user, User):
            user.restore()
            user_id = user.id

        async with self._pool() as session:
            sql = update(db.User).where(id=user_id).values(deleted_at=None)
            await session.execute(sql)
            await session.commit()

    async def delete_user(self, user: User | int):
        db_user: db.User = None
        if isinstance(user, User):
            user.delete()
            db_user = db.User.from_domain(user)
        else:
            db_user = db.User(id=user, deleted_at=datetime.now())

        async with self._pool() as session:
            await session.merge(db_user)
            await session.commit()
