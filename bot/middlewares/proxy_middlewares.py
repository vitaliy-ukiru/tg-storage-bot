__all__ = (
    'BaseMiddleware',
    'CategoryProxyMiddleware',
    'FileProxyMiddleware'
)

from typing import Callable, Any, Awaitable, Dict, Union, TypeVarTuple, TypeVar, Generic

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core.domain.services.category import CategoryUsecase
from core.domain.services.file import FileUsecase

UsecaseT = TypeVar('UsecaseT', CategoryUsecase, FileUsecase)

class BaseProxyMiddleware(Generic[UsecaseT], BaseMiddleware):
    key: str
    svc: UsecaseT

    def __init__(self, svc: UsecaseT):
        self.svc = svc

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        data[self.key] = self.svc
        return await handler(event, data)


class CategoryProxyMiddleware(BaseProxyMiddleware[CategoryUsecase]):
    key = "category_service"


class FileProxyMiddleware(BaseProxyMiddleware[FileUsecase]):
    key = "file_service"

