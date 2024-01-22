__all__ = (
    'UserUsecase',
)
from abc import abstractmethod
from typing import Protocol

from app.core.domain.dto.user import CreateUserDTO, UpdateLocaleDTO
from app.core.domain.models.user import UserId, User


class UserUsecase(Protocol):
    @abstractmethod
    async def create_user(self, dto: CreateUserDTO) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: UserId, force_find: bool = False) -> User:
        raise NotImplementedError

    @abstractmethod
    async def update_locale(self, dto: UpdateLocaleDTO) -> User:
        raise NotImplementedError

