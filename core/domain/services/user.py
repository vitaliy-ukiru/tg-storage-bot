import abc
from datetime import datetime
from typing import Protocol, cast, Optional

from core.domain.exceptions.user import UserNotFound, UserDeleted
from core.domain.models.user import User, UserId


class UserRepository(Protocol):

    @abc.abstractmethod
    async def save_user(self, user_id: UserId) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user(self, user_id: UserId) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def restore_user(self, user_id: UserId) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_user(self, user: UserId) -> Optional[User]:
        raise NotImplementedError


class UserService:
    _repo: UserRepository

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def create_user(self, user_id: UserId) -> User:
        return await self._repo.save_user(user_id)

    async def get_user(self, user_id: UserId, update_on_error: bool = False) -> User:
        user = await self._repo.get_user(user_id)
        if user is None:
            if not update_on_error:
                raise UserNotFound(user_id)
            user = self._repo.save_user(user_id)

        if user.is_deleted:
            if not update_on_error:
                raise UserDeleted(user_id)

            user = await self._repo.restore_user(user_id)

        return user
