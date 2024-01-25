__all__ = (
    'UserUsecase',
    'UserCreator', 'UserGetter', 'UserUpdater',
)

from abc import abstractmethod
from typing import Protocol

from app.core.domain.dto.user import CreateUserDTO, UpdateLocaleDTO
from app.core.domain.models.user import UserId, User


class UserCreator(Protocol):
    @abstractmethod
    async def create_user(self, dto: CreateUserDTO) -> User:
        raise NotImplementedError


class UserGetter(Protocol):
    @abstractmethod
    async def get_user(self, user_id: UserId, restore: bool = False) -> User:
        raise NotImplementedError


class UserUpdater(Protocol):
    @abstractmethod
    async def update_locale(self, dto: UpdateLocaleDTO) -> User:
        raise NotImplementedError


class UserUsecase(
    Protocol,
    UserCreator, UserGetter, UserUpdater,
):
    pass
