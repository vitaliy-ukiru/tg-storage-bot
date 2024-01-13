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

from app.bot.states.dialogs import FileListSG
from app.bot.utils.file_type_str import file_categories_with_names
from app.bot.widgets import BACK_TEXT
from app.core.domain.models.file import FileCategory
from .common import ID_SELECT_FILE_TYPES


class FileTypeItem(NamedTuple):
    name: str
    value: FileCategory


file_types_window = Window(
    Const("Выберите тип файла"),
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
    getter={
        "file_types": [
            FileTypeItem(name=name, value=file_type_category)
            for name, file_type_category in file_categories_with_names()
        ]
    },
)
