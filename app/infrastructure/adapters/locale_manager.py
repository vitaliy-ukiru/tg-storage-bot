from typing import Protocol, Optional

from aiogram.types import User as TelegramUser
from aiogram_i18n.managers import BaseManager

from app.core.domain.dto.user import UpdateLocaleDTO
from app.core.domain.models.user import UserId, User
from app.core.interfaces.usecase.user import UserGetter, UserUpdater


class UserGateway(
    Protocol, UserGetter, UserUpdater
):
    pass


class LazyLocaleManager(BaseManager):
    def __init__(self, user_gateway: UserGateway, default_locale: Optional[str] = None) -> None:
        self._user_gateway = user_gateway
        super().__init__(default_locale)

    async def set_locale(self,
                         locale: str,
                         user: User,
                         event_from_user: TelegramUser,
                         ) -> None:
        user_id = UserId(event_from_user.id)
        if user is not None:
            user_id = user.id
        await self._user_gateway.update_locale(
            UpdateLocaleDTO(
                user_id=user_id,
                locale=locale,
            )
        )
        user.locale = locale

    async def get_locale(self,
                         event_from_user: TelegramUser,
                         user: Optional[User] = None,
                         ) -> str:
        if user:
            return user.locale

        if not event_from_user:
            return self.default_locale

        user = await self._user_gateway.get_user(UserId(event_from_user.id), restore=True)
        return user.locale
