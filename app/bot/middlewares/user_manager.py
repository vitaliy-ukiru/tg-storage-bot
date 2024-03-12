__all__ = (
    'UserMiddleware',
    'USER_KEY',
    'ACCESS_CONTROLLER_KEY'
)

from typing import Callable, Dict, Any, Awaitable, cast

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.types import TelegramObject, User as TgUser

from app.core.domain.dto.user import CreateUserDTO
from app.core.domain.exceptions.user import UserNotFound
from app.core.domain.models.user import UserId
from app.core.interfaces.usecase import UserUsecase
from app.infrastructure.adapters.auth.telegram import TelegramAccessController

USER_KEY = "user"
ACCESS_CONTROLLER_KEY = "access_controller"


class UserMiddleware(BaseMiddleware):
    def __init__(self, svc: UserUsecase):
        self.svc = svc

    async def _get_user(self, tg_user: TgUser):
        user_id = tg_user.id
        try:
            user = await self.svc.get_user(UserId(user_id), restore=True)
        except UserNotFound:
            user = await self.svc.create_user(
                CreateUserDTO(
                    user_id=user_id,
                    locale=tg_user.language_code,
                )
            )

        return user

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        tg_user = cast(TgUser | None, data.get(EVENT_FROM_USER_KEY))
        if tg_user is None:
            return await handler(event, data)

        user = await self._get_user(tg_user)
        data[USER_KEY] = user
        data[ACCESS_CONTROLLER_KEY] = TelegramAccessController(user.id)
        return await handler(event, data)
