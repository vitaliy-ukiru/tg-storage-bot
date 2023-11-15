import enum
from abc import ABC

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup

from bot.ui import common
from bot.ui.telegram_component import TelegramMarkup
from core.domain.category import Category


class CategoryViewMarkup(TelegramMarkup, ABC):
    category: Category

    def __init__(self, category: Category):
        self.category = category

    def build(self) -> InlineKeyboardMarkup:
        return common.create_markup(
            (
                ("Изменить имя", CategoryViewAction.edit_name),
                ("Изменить описание", CategoryViewAction.edit_desc),
                ("Файлы", CategoryViewAction.files_list)
            ),
            CategoryViewData,
            "action",
            category_id=self.category.id
        )


class CategoryViewAction(enum.StrEnum):
    edit_name = enum.auto()
    edit_desc = enum.auto()
    files_list = enum.auto


class CategoryViewData(CallbackData, prefix="category_view"):
    action: CategoryViewAction
    category_id: int
