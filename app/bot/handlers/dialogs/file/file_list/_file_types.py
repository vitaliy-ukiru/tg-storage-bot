__all__ = (
    'file_types_window',
    'FileTypeItem'
)

from typing import NamedTuple

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import (
    Back, Group, Multiselect,
    ManagedMultiselect
)
from aiogram_dialog.widgets.text import Const, Format

from app.bot.states.dialogs import FileListSG
from app.bot.utils.file_type_str import file_types_with_names
from app.bot.widgets import BACK_TEXT
from app.core.domain.models.file import FileType
from .common import ID_SELECT_FILE_TYPES


class FileTypeItem(NamedTuple):
    name: str
    value: FileType


file_types_window = Window(
    Const("Выберите тип файла"),
    Group(
        Multiselect(
            Format("✓ {item.name}"),
            Format("{item.name}"),
            id=ID_SELECT_FILE_TYPES,
            type_factory=lambda s: FileType(s),
            item_id_getter=lambda file_type: file_type.value,
            items="file_types",
        ),
        width=1,
    ),
    Back(BACK_TEXT),
    state=FileListSG.input_file_type,
    getter={
        "file_types": [
            FileTypeItem(name=name, value=ft)
            for name, ft in file_types_with_names()
        ]
    },
)
