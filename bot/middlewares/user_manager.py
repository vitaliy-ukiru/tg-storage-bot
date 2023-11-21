__all__ = (
    'UserMiddleware',
    'USER_KEY',
)
from typing import Callable, Dict, Any, Awaitable, cast

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.types import TelegramObject, User as TgUser

from core.domain.user.service import UserUseCase

USER_KEY = "user_obj"


class UserMiddleware(BaseMiddleware):
    def __init__(self, svc: UserUseCase):
        self.svc = svc

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        tg_user = cast(TgUser | None, data.get(EVENT_FROM_USER_KEY))
        user_id = tg_user.id
        user = await self.svc.get_user(user_id, True)
        data[USER_KEY] = user
        data["user_service"] = self.svc
        return await handler(event, data)
