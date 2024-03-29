__all__ = (
    'UserStorageGateway',
)

from datetime import datetime
from typing import Optional

from asyncpg import UniqueViolationError

from app.core.domain.exceptions.user import UserAlreadyExists
from app.core.domain.models.user import User
from app.core.interfaces.repository.user import (
    UserRepoSaver, UserRepoGetter, UserRepoUpdater, UserRepoDeleter
)
from app.infrastructure.db import models
from app.infrastructure.db.repo._base import BaseRepository


class UserStorageGateway(
    UserRepoSaver, UserRepoGetter, UserRepoUpdater, UserRepoDeleter,
    BaseRepository
):
    async def save_user(self, user_id: int, locale: Optional[str] = None) -> User:
        async with self._pool() as session:
            db_user = models.User(id=user_id, locale=locale)
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
            db_user: models.User | None = await session.get(models.User, user_id)
            if db_user is None:
                return None

            return db_user.to_domain()

    async def update_locale(self, user: User):
        async with self._pool() as session:
            model: models.User | None = await session.get(models.User, user.id)
            if model is None:
                return

            model.locale = user.locale
            await session.commit()

    async def restore_user(self, user_id: int) -> Optional[User]:
        async with self._pool() as session:
            user: models.User | None = await session.get(models.User, user_id)
            if user is None:
                return None

            user.deleted_at = None
            await session.commit()
            return user.to_domain()

    async def delete_user(self, user_id: int) -> Optional[User]:
        async with self._pool() as session:
            user: models.User | None = await session.get(models.User, user_id)
            if user is None:
                return None

            user.deleted_at = datetime.now()
            await session.commit()
            return user.to_domain()
