import enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup

from .. import common
from bot.ui.telegram_component import TelegramMarkup


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
        return common.create_markup(markup, FileEditAction, "scope", file_id=self._file_id)


class EditScope(enum.StrEnum):
    title = enum.auto()
    category = enum.auto()
    upload = enum.auto()


class FileEditAction(CallbackData, prefix="file_edit"):
    scope: EditScope
    file_id: int
