from typing import Iterable, Type

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_markup(
    buttons: Iterable[tuple[str, str]], factory: Type[CallbackData],
    data_key: str,
    **defaults
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=text,
                callback_data=factory(**({data_key: data} | defaults.copy())).pack()
            )
        ]
        for text, data in buttons
    ])
