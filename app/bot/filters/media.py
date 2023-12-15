from typing import Any, Union, Dict

from aiogram.enums import ContentType
from aiogram.filters import Filter
from aiogram.types import Message

MEDIA_CONTENT_TYPES = frozenset((
    ContentType.PHOTO,
    ContentType.DOCUMENT,
    ContentType.AUDIO,
    ContentType.VIDEO,
    ContentType.ANIMATION,
))


class MediaFilter(Filter):
    async def __call__(self, msg: Message) -> Union[bool, Dict[str, Any]]:
        return msg.content_type in MEDIA_CONTENT_TYPES
