from abc import abstractmethod
from typing import cast, Protocol

from app.core.domain.dto.user import CreateUserDTO, UpdateLocaleDTO
from app.core.domain.exceptions.user import UserNotFound, UserDeleted, UnknownLocale
from app.core.domain.models.user import User, UserId
from app.core.interfaces.repository.user import (
    UserRepoSaver, UserRepoGetter, UserRepoDeleter, UserRepoUpdater
)
from app.core.interfaces.usecase.user import UserUsecase


class LocaleValidator(Protocol):
    @abstractmethod
    def validate_locale(self, locale: str) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def default_locale(self) -> str:
        raise NotImplementedError

class UserService(UserUsecase):
    _saver: UserRepoSaver
    _getter: UserRepoGetter
    _updater: UserRepoUpdater
    _deleter: UserRepoDeleter

    def __init__(
        self,
        saver: UserRepoSaver,
        getter: UserRepoGetter,
        updater: UserRepoUpdater,
        deleter: UserRepoDeleter,
        locale_validator: LocaleValidator,
    ):

        self._saver = saver
        self._getter = getter
        self._updater = updater
        self._deleter = deleter
        self._locale_validator = locale_validator

    async def create_user(self, dto: CreateUserDTO) -> User:
        locale = dto.locale
        if locale is not None:
            if not self._locale_validator.validate_locale(locale):
                raise UnknownLocale(dto.user_id, locale)
        else:
            locale = self._locale_validator.default_locale

        return await self._saver.save_user(UserId(dto.user_id), locale)

    async def get_user(self, user_id: UserId, restore: bool = False) -> User:
        user = await self._getter.get_user(user_id)
        if user is None:
            raise UserNotFound(user_id)

        if user.is_deleted:
            if not restore:
                raise UserDeleted(user_id)

            user = await self._deleter.restore_user(user_id)

        return cast(User, user)

    async def update_locale(self, dto: UpdateLocaleDTO) -> User:
        user = await self._getter.get_user(UserId(dto.user_id))
        if not self._locale_validator.validate_locale(dto.locale):
            raise UnknownLocale(dto.user_id, dto.locale)
        user.locale = dto.locale

        await self._updater.update_locale(user)
        return user

