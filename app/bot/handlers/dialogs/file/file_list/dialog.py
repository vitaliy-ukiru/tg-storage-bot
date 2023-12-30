__all__ = (
    'file_list_dialog',
)

from typing import Any

from aiogram_dialog import Dialog, DialogManager, Data
from aiogram_dialog.widgets.kbd import ManagedMultiselect

from app.core.domain.models.file import FileType
from .common import SELECT_FILE_TYPES_ID
from ._main import main_window
from ._file_types import FileTypeItem, file_types_window
from ._title import input_title_window
from ._results_list import results_window


async def _on_start(start_data: dict | Any, manager: DialogManager):
    if not isinstance(start_data, dict):
        return

    filters: dict = start_data.get("filters")
    if filters is None:
        return

    file_types = filters.get('file_types')
    if file_types is not None:
        select: ManagedMultiselect[FileType] = manager.find(SELECT_FILE_TYPES_ID)
        for file_type in file_types:
            if isinstance(file_type, FileTypeItem):
                file_type = file_type.value
            await select.set_checked(file_type, False)

    manager.dialog_data["filters"] = filters


async def _on_process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        filters = manager.dialog_data.setdefault("filters", {})
        filters["category_id"] = result["category_id"]


file_list_dialog = Dialog(
    main_window,
    file_types_window,
    input_title_window,
    results_window,
    on_start=_on_start,
    on_process_result=_on_process_result
)
