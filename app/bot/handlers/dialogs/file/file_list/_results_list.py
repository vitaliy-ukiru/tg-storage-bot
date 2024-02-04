__all__ = (
    'results_window',
)

from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Select, StubScroll, Column
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from app.bot.handlers.dialogs import execute
from app.bot.handlers.dialogs.file.file_list.common import tl_file_list
from app.bot.handlers.dialogs.file.file_list.filters_dao import FiltersDAO
from app.bot.services import Paginator
from app.bot.states.dialogs import FileListSG
from app.bot.widgets import BackTo
from app.bot.widgets.i18n import BACK_TEXT
from app.bot.widgets.i18n.file_title import FileTitle
from app.bot.widgets.scroll import Navigation
from app.core.domain.models.user import User
from app.core.interfaces.usecase.file import FileUsecase

FILE_LIST_ID = "file_list"
FILES_PER_PAGE = 7


async def _files_find_getter(dialog_manager: DialogManager, file_service: FileUsecase, user: User, **_):
    filters_dao = FiltersDAO(dialog_manager)
    filters = filters_dao.extract_to_dto(user.id)

    pager: ManagedScroll = dialog_manager.find(FILE_LIST_ID)
    current_page = await pager.get_page()
    paginator = Paginator(FILES_PER_PAGE, current_page)

    files, total_files = await file_service.find_files(
        dto=filters,
        paginate=paginator.pagination,
        total_count=True
    )
    return {
        "pages": paginator.get_page_count(total_files),
        "files": files,
    }


async def _process_click_file(_, __, manager: DialogManager, item_id: int):
    await execute.file_view(manager, item_id, data=dict(opened_over=True), mode=StartMode.NORMAL)


results_window = Window(
    tl_file_list.result.select(),
    Column(
        Select(
            FileTitle(
                Format("{item.title}"),
                F["item"].id,
                F["item"].title
            ),
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
