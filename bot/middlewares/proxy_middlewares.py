__all__ = (
    'BaseMiddleware',
    'CategoryProxyMiddleware',
    'FileProxyMiddleware'
)
from typing import Callable, Any, Awaitable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.domain.category import CategoryUseCase
from core.domain.file.service import FileUseCase

Domain = Union[CategoryUseCase, FileUseCase]


class BaseProxyMiddleware(BaseMiddleware):
    key: str
    svc: Domain

    def __init__(self, svc: Domain):
        self.svc = svc

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        data[self.key] = self.svc
        return await handler(event, data)


class CategoryProxyMiddleware(BaseProxyMiddleware):
    key = "category_service"

    def __init__(self, svc: CategoryUseCase):
        super().__init__(svc)


class FileProxyMiddleware(BaseProxyMiddleware):
    key = "file_service"

    def __init__(self, svc: FileUseCase):
        super().__init__(svc)

