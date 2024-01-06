__all__ = (
    'file_list_dialog',
)

from typing import Any

from aiogram_dialog import Dialog, DialogManager, Data

from ._file_types import file_types_window
from ._main import main_window
from ._results_list import results_window
from ._title import input_title_window
from .common import FiltersDict
from .filters_dao import FiltersDAO


async def _on_start(start_data: dict | Any, manager: DialogManager):
    if not isinstance(start_data, dict):
        return

    filters: FiltersDict = start_data.get("filters")
    if filters is None:
        return

    filters_dao = FiltersDAO(manager)
    await filters_dao.setup(filters)


async def _on_process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        filters = FiltersDAO(manager)
        filters.category = result["category_id"]


file_list_dialog = Dialog(
    main_window,
    file_types_window,
    input_title_window,
    results_window,
    on_start=_on_start,
    on_process_result=_on_process_result
)
