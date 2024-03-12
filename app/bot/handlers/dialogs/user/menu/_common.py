from typing import Callable, Awaitable

from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.bot.widgets.i18n import TemplateProxy

TL = TemplateProxy("user", "menu")


async def _number_filter(m: Message):
    return m.text.isdigit()  # id can't be less than zero, don't test negative case


def _error_getter(error_key: str) -> Callable[[...], Awaitable[dict]]:
    async def _getter(dialog_manager: DialogManager, **_):
        err = dialog_manager.dialog_data.pop(error_key, None)
        if not err or not isinstance(err, Exception):
            return {}

        return {
            "error_type": type(err),
            "error": err,
        }

    return _getter
