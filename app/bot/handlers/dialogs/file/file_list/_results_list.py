__all__ = (
    'results_window',
)

import math
from typing import Any

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, StubScroll, Column
from aiogram_dialog.widgets.text import Const, Format

from app.bot.handlers.dialogs import execute
from app.bot.middlewares.user_manager import USER_KEY
from app.bot.states.dialogs import FileListSG
from app.bot.widgets import BackTo, BACK_TEXT
from app.bot.widgets.scroll import Navigation
from app.core.domain.dto.common import Pagination
from app.core.domain.dto.file import FilesFindDTO
from app.core.domain.models.user import User
from app.core.interfaces.usecase.file import FileUsecase

FILE_LIST_ID = "file_list"
FILES_PER_PAGE = 7

def _to_dto(user_id: int, filters: dict[str, Any]) -> FilesFindDTO:
    return FilesFindDTO(
        user_id=user_id,
        category_id=filters.get('category_id'),
        file_types=filters.get('file_types'),
        title_match=filters.get('title'),
    )


async def _files_find_getter(dialog_manager: DialogManager, file_service: FileUsecase, **_):

    user: User = dialog_manager.middleware_data[USER_KEY]
    filters = _to_dto(user.id, dialog_manager.dialog_data.get("filters", {}))
    current_page = await dialog_manager.find(FILE_LIST_ID).get_page()

    files, total_files = await file_service.find_files(
        dto=filters,
        paginate=Pagination(
            FILES_PER_PAGE,
            current_page * FILES_PER_PAGE,
        ),
        total_count=True
    )
    return {
        "pages": math.ceil(total_files / FILES_PER_PAGE),
        "files": files,
    }


async def _process_click_file(_, __, manager: DialogManager, item_id: int):
    await execute.file_view(manager, item_id, data=dict(opened_over=True))


results_window = Window(
    Const("Выберите файл из списка"),
    Column(
        Select(
            Format("{item.title}"),
            id="select_file",
            type_factory=int,
            on_click=_process_click_file,
            item_id_getter=lambda file: file.id,
            items="files",
        )
    ),
    Navigation(FILE_LIST_ID),
    StubScroll(
        id=FILE_LIST_ID,
        pages="pages",
    ),
    BackTo(FileListSG.main, BACK_TEXT),
    state=FileListSG.file_list,
    getter=_files_find_getter
)
