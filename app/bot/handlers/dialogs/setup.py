from aiogram import Router

from app.bot.handlers.dialogs.category import (category_create_dialog, category_select_dialog,
                                               find_category_dialog, category_edit_dialog)
from app.bot.handlers.dialogs.file import file_edit_dialog, file_view_dialog, file_list_dialog
from app.bot.handlers.dialogs.user import user_change_locale


def _router() -> Router:
    r = Router()
    r.include_routers(user_change_locale)
    r.include_routers(file_view_dialog, file_edit_dialog, find_category_dialog)
    r.include_routers(category_select_dialog, category_create_dialog, category_edit_dialog)
    r.include_routers(file_list_dialog)
    return r

def setup(r: Router):
    r.include_router(_router())
