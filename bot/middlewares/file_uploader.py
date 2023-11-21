__all__ = (
    'FileUploaderMiddleware',
)
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.utils.uploader import FileUploader
from core.domain.file.service import FileUseCase


class FileUploaderMiddleware(BaseMiddleware):
    def __init__(self, svc: FileUseCase):
        self._uploader = FileUploader(svc)

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        data["uploader"] = self._uploader
        return await handler(event, data)
