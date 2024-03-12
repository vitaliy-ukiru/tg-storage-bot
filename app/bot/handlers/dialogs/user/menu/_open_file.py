from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import DialogManager, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Case

from app.bot.middlewares.user_manager import ACCESS_CONTROLLER_KEY
from app.bot.states.dialogs import FileViewSG, UserMenuSG
from app.bot.widgets.i18n import Template, BackToI18n
from app.core.domain.exceptions.file import FileNotFound, FileAccessDenied
from app.core.domain.models.file import FileId
from app.core.domain.models.user import User
from app.core.interfaces.usecase import FileUsecase
from ._common import TL, _number_filter, _error_getter
from ... import execute

OPEN_FILE_ERROR_KEY = "open_file_error"


async def _on_input_file(m: Message, _, manager: DialogManager):
    file_id = FileId(int(m.text))
    file_service: FileUsecase = manager.middleware_data["file_service"]
    ac = manager.middleware_data[ACCESS_CONTROLLER_KEY]

    try:
        file = await file_service.get_file(file_id, ac)
    except (FileNotFound, FileAccessDenied) as exp:
        manager.dialog_data[OPEN_FILE_ERROR_KEY] = exp
        return

    await execute.file_view(manager, file.id, mode=StartMode.NORMAL)


open_file_window = Window(

    Case(
        {
            FileNotFound: Template("file-not-found"),
            FileAccessDenied: Template("file-access-denied"),
        },
        selector="error_type",
        when="error_type"
    ),
    TL.file.enter(),
    MessageInput(_on_input_file, ContentType.TEXT, _number_filter),
    BackToI18n(UserMenuSG.main),
    state=UserMenuSG.open_file,
    getter=_error_getter(OPEN_FILE_ERROR_KEY),
)
