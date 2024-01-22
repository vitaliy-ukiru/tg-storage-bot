from abc import abstractmethod
from typing import Protocol, Any, Optional

from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.types import User as TelegramUser
from aiogram_i18n.managers import BaseManager

from app.bot.middlewares.user_manager import USER_KEY
from app.core.domain.dto.user import UpdateLocaleDTO
from app.core.domain.models.user import UserId, User


class UserGateway(Protocol):

    @abstractmethod
    async def update_locale(self, dto: UpdateLocaleDTO) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: UserId, force_find: bool = False) -> User:
        raise NotImplementedError


class GatewayLocaleManager(BaseManager):
    def __init__(self, user_gateway: UserGateway, default_locale: Optional[str] = None) -> None:
        self._user_gateway = user_gateway
        super().__init__(default_locale)

    async def set_locale(self, locale: str, event_from_user: TelegramUser) -> None:
        await self._user_gateway.update_locale(
            UpdateLocaleDTO(
                user_id=event_from_user.id,
                locale=locale,
            )
        )

    async def get_locale(self, event_from_user: Optional[TelegramUser] = None) -> str:
        if not event_from_user:
            return self.default_locale

        user = await self._user_gateway.get_user(UserId(event_from_user.id), force_find=True)
        return user.locale


class ContextLocaleManager(BaseManager):

    async def set_locale(self, locale: str, user: Optional[User] = None) -> None:
        if not user:
            return
        # it will mutate user in context data for
        # handler
        user.locale = locale

    async def get_locale(self, user: Optional[User] = None) -> str:
        if not user:
            return self.default_locale

        return user.locale


class LazyGatewayLocaleManager(BaseManager):
    def __init__(
        self,
        gateway_manager: GatewayLocaleManager,
        ctx_manager: ContextLocaleManager,
        default_locale: Optional[str] = None
    ) -> None:
        self.ctx_manager = ctx_manager
        self.gateway_manager = gateway_manager
        super().__init__(default_locale)

    @property
    def default_locale(self) -> str:
        return super().default_locale

    @default_locale.setter
    def default_locale(self, value: str):
        super().default_locale = value
        self.ctx_manager.default_locale = value
        self.gateway_manager.locale_setter = value

    async def set_locale(self,
                         locale: str,
                         *args, **kwargs
                         ) -> None:
        await self.ctx_manager.set_locale(locale, kwargs.get(USER_KEY))
        await self.gateway_manager.set_locale(locale, kwargs.get(EVENT_FROM_USER_KEY))

    async def get_locale(self,
                         event_from_user: TelegramUser,
                         user: Optional[User] = None,
                         ) -> str:
        if user:
            return await self.ctx_manager.get_locale(user)

        return await self.gateway_manager.get_locale(event_from_user)
