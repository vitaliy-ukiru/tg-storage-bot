from typing import cast

from app.core.common.locales import ensure_locale
from app.core.domain.dto.user import CreateUserDTO, UpdateLocaleDTO
from app.core.interfaces.repository.user import (
    UserSaver, UserGetter, UserDeleter, UserUpdater
)
from app.core.interfaces.usecase.user import UserUsecase
from app.core.domain.exceptions.user import UserNotFound, UserDeleted
from app.core.domain.models.user import User, UserId


class UserService(UserUsecase):
    _saver: UserSaver
    _getter: UserGetter
    _updater: UserUpdater
    _deleter: UserDeleter

    def __init__(
        self,
        saver: UserSaver,
        getter: UserGetter,
        updater: UserUpdater,
        deleter: UserDeleter
    ):

        self._saver = saver
        self._getter = getter
        self._updater = updater
        self._deleter = deleter

    async def create_user(self, dto: CreateUserDTO) -> User:
        locale = ensure_locale(dto.locale)
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
        user.locale = ensure_locale(dto.locale)
        await self._updater.update_locale(user)
        return user
