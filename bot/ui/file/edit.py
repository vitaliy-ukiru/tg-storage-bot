import enum

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup

from .. import common, TelegramComponent
from bot.ui.telegram_component import TelegramMarkup

class FileEdit(TelegramComponent):
    _file_id: int

    def __init__(self, file_id: int):
        self._file_id = file_id

    @property
    def text(self):
        return "Что будем редактировать?"

    @property
    def markup(self):
        markup = FileEditMarkup(self._file_id)
        return markup.build()

    async def send(self, bot: Bot, chat_id: int):
        return await bot.send_message(chat_id, self.text, reply_markup=self.markup)


class FileEditMarkup(TelegramMarkup):
    _file_id: int

    def __init__(self, file_id: int):
        self._file_id = file_id

    def build(self) -> InlineKeyboardMarkup:
        markup = (
            ("Изменить название", EditScope.title),
            ("Изменить категорию", EditScope.category),
            ("Перезагрузить файл", EditScope.upload),
        )
        return common.create_markup(markup, FileEditFactory, "scope", file_id=self._file_id)


class EditScope(enum.StrEnum):
    title = enum.auto()
    category = enum.auto()
    upload = enum.auto()


class FileEditFactory(CallbackData, prefix="file_edit"):
    scope: EditScope
    file_id: int
