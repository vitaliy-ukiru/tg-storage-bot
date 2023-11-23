from datetime import datetime
from typing import Optional

from asyncpg import UniqueViolationError
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.domain.services.user import UserRepository as Repository
from core.domain.models.user import User
from core.domain.exceptions.user import UserAlreadyExists, UserNotFound, UserDeleted

from .database.models import User as UserModel


class UserGateway(Repository):
    _pool: async_sessionmaker

    def __init__(self, session_maker: async_sessionmaker):
        self._pool = session_maker

    async def save_user(self, user_id: int) -> User:
        async with self._pool() as session:
            db_user = UserModel(id=user_id)
            try:
                session.add(db_user)
                await session.commit()
            except UniqueViolationError:
                await session.rollback()
                raise UserAlreadyExists(user_id)
            else:
                return db_user.to_domain()

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self._pool() as session:
            db_user: UserModel | None = await session.get(UserModel, user_id)
            if db_user is None:
                return None

            return db_user.to_domain()

    async def restore_user(self, user_id: int) -> Optional[User]:
        async with self._pool() as session:
            user: UserModel | None = await session.get(UserModel, user_id)
            if user is None:
                return None

            user.deleted_at = None
            await session.commit()
            return user.to_domain()

    async def delete_user(self, user_id: int) -> Optional[User]:
        async with self._pool() as session:
            user: UserModel | None = await session.get(UserModel, user_id)
            if user is None:
                return None

            user.deleted_at = datetime.now()
            await session.commit()
            return user.to_domain()
