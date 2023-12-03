from aiogram import Router

from bot.handlers.dialogs.category import (category_create_dialog, category_select_dialog,
                                           find_category_dialog)
from bot.handlers.dialogs.file import file_edit_dialog, file_view_dialog, filter_select_dialog
from bot.handlers.dialogs.file.file_list import file_list_dialog


def router() -> Router:
    r = Router()
    r.include_routers(file_view_dialog, file_edit_dialog, find_category_dialog)
    r.include_routers(category_select_dialog, category_create_dialog)
    r.include_routers(filter_select_dialog, file_list_dialog)
    return r
