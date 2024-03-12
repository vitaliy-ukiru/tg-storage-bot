from aiogram import Router

from .category import category_create_dialog, find_category_dialog, category_edit_dialog
from .file import file_edit_dialog, file_view_dialog, file_list_dialog, file_upload_dialog
from .user import user_change_locale, user_menu_dialog


def _router() -> Router:
    r = Router()
    r.include_routers(
        user_menu_dialog,
        user_change_locale
    )
    r.include_routers(
        file_view_dialog,
        file_edit_dialog,
        find_category_dialog,
        file_upload_dialog
    )

    r.include_routers(
        category_create_dialog,
        category_edit_dialog
    )
    r.include_routers(file_list_dialog)
    return r


def setup(r: Router):
    r.include_router(_router())
