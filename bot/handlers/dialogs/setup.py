from aiogram import Router

from bot.handlers.dialogs.category import (category_create_dialog, category_select_dialog,
                                           find_category_dialog)
from bot.handlers.dialogs.file import file_edit_dialog, file_view_dialog


def router() -> Router:
    r = Router()
    r.include_router(file_view_dialog)
    r.include_router(file_edit_dialog)
    r.include_router(find_category_dialog)
    r.include_router(category_select_dialog),
    r.include_router(category_create_dialog),
    return r
