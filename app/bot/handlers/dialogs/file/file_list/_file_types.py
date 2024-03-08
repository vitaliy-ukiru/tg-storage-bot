__all__ = (
    'file_types_window',

)

from operator import itemgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Back, Group, Multiselect
)
from aiogram_dialog.widgets.text import Format
from aiogram_i18n import I18nContext

from app.bot.states.dialogs import FileListSG
from app.bot.utils import file_categories_with_names
from app.bot.widgets.i18n import BACK_TEXT
from app.core.domain.models.file import FileCategory
from .common import ID_SELECT_FILE_TYPES, tl_file_list


async def _file_types_getter(i18n: I18nContext, **_):
    return {
        "file_types": file_categories_with_names(i18n)
    }


file_types_window = Window(
    tl_file_list.type.select(),
    Group(
        Multiselect[FileCategory](
            Format("✓ {item[0]}"),
            Format("{item[0]}"),
            id=ID_SELECT_FILE_TYPES,
            type_factory=FileCategory,
            item_id_getter=itemgetter(1),
            items="file_types",
        ),
        width=1,
    ),
    Back(BACK_TEXT),
    state=FileListSG.input_file_type,
    getter=_file_types_getter
)
