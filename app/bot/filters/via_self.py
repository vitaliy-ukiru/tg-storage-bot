from typing import Any, Union, Dict

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import Message


class ViaSelfRestrict(Filter):
    async def __call__(self, msg: Message, bot: Bot) -> Union[bool, Dict[str, Any]]:
        via_bot = msg.via_bot
        if via_bot is None:
            return True

        return via_bot.id != bot.id
