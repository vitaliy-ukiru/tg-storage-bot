from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.kbd import Start, Select, Back, ScrollingGroup, Next
from aiogram_dialog.widgets.text import Const, Format

from bot.handlers.dialogs import execute
from bot.handlers.dialogs.file.filter_select import filters_text
from bot.handlers.dialogs.start_data import StartWithData
from bot.middlewares.user_manager import USER_KEY
from bot.states.dialogs import FilterSG, FileListSG
from core.domain.dto.file import FilterDTO
from core.domain.models.user import User
from core.domain.services.file import FileUsecase


async def _process_click_file(_: CallbackQuery, __: Select, manager: DialogManager, item_id: int):
    await execute.file_view(manager, item_id, data=dict(opened_over=True))


def _to_dto(user_id: int, filters: dict[str, Any]) -> FilterDTO:
    return FilterDTO(
        user_id=user_id,
        category_id=filters.get('category_id'),
        file_type=filters.get('file_type'),
        title_match=filters.get('title'),
    )


async def _on_process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        manager.dialog_data["filters"] = result.get("filters", {}).copy()


async def _on_start(start_data: dict | Any, manager: DialogManager):
    if not isinstance(start_data, dict):
        return

    manager.dialog_data["filters"] = start_data.get("filters", {})


async def _files_find_getter(dialog_manager: DialogManager, file_service: FileUsecase, **_):
    user: User = dialog_manager.middleware_data[USER_KEY]
    filters = _to_dto(user.id, dialog_manager.dialog_data.get("filters", {}))
    files = await file_service.find_files(dto=filters)
    return {
        "files": files,
    }


async def _filters_start_getter(dialog_manager: DialogManager, **_):
    filters = dialog_manager.dialog_data.get("filters")
    if filters is not None:
        filters = filters.copy()

    return {
        "filters": filters,
    }


file_list_dialog = Dialog(
    Window(
        Const("Список"),
        filters_text,
        StartWithData(
            Const("Фильтры"),
            id="file_select_open",
            state=FilterSG.main,
            getter=_filters_start_getter
        ),
        Next(Const("🔎 Поиск")),
        state=FileListSG.main
    ),

    Window(
        Const("Выберите файл из списка"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="select_file",
                type_factory=int,
                on_click=_process_click_file,
                item_id_getter=lambda file: file.id,
                items="files",
            ),
            id="file_list",
            width=1,
            height=7
        ),
        Back(),
        state=FileListSG.file_list,
        getter=_files_find_getter
    ),
    on_start=_on_start,
    on_process_result=_on_process_result
)
