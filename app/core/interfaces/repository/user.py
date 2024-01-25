__all__ = (
    'UserSaver',
    'UserGetter',
    'UserUpdater',
    'UserDeleter',
)

import abc
from typing import Protocol, Optional

from app.core.domain.models.user import UserId, User


class UserSaver(Protocol):

    @abc.abstractmethod
    async def save_user(self, user_id: UserId, locale: Optional[str] = None) -> User:
        raise NotImplementedError


class UserGetter(Protocol):
    @abc.abstractmethod
    async def get_user(self, user_id: UserId) -> Optional[User]:
        raise NotImplementedError


class UserUpdater(Protocol):
    @abc.abstractmethod
    async def update_locale(self, user: User):
        raise NotImplementedError


class UserDeleter(Protocol):
    @abc.abstractmethod
    async def restore_user(self, user_id: UserId) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_user(self, user: UserId) -> Optional[User]:
        raise NotImplementedError
