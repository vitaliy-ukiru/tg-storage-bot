import abc

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


class TelegramComponent(abc.ABC):
    @abc.abstractmethod
    async def send(self, bot: Bot, chat_id: int):
        raise NotImplemented()


class TelegramMarkup(abc.ABC):
    @abc.abstractmethod
    def build(self) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
        raise NotImplemented
