__all__ = (
    'file_types_window',
    'FileTypeItem'
)

from typing import NamedTuple

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Back, Group, Multiselect
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_i18n import I18nContext

from app.bot.states.dialogs import FileListSG
from app.bot.utils.file_type_i18n import file_categories_with_names
from app.bot.widgets.i18n import BACK_TEXT, Template
from app.core.domain.models.file import FileCategory
from .common import ID_SELECT_FILE_TYPES, lc_file_list


class FileTypeItem(NamedTuple):
    name: str
    value: FileCategory


async def _file_types_getter(i18n: I18nContext, **_):
    return {
        "file_types": [
            FileTypeItem(name=name, value=file_type_category)
            for name, file_type_category in file_categories_with_names(i18n)
        ]
    }


file_types_window = Window(
    Template(lc_file_list.type.select),
    Group(
        Multiselect(
            Format("✓ {item.name}"),
            Format("{item.name}"),
            id=ID_SELECT_FILE_TYPES,
            type_factory=lambda s: FileCategory(s),
            item_id_getter=lambda file_type: file_type.value,
            items="file_types",
        ),
        width=1,
    ),
    Back(BACK_TEXT),
    state=FileListSG.input_file_type,
    getter=_file_types_getter
)
