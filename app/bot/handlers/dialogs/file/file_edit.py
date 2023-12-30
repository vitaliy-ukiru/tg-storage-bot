from typing import Any

from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Const

from app.bot.filters.media import MediaFilter
from app.bot.widgets import BackTo, CANCEL_TEXT, CLOSE_TEXT
from app.bot.widgets import StartWithData
from app.bot.middlewares.user_manager import USER_KEY
from app.bot.states.dialogs import FileEditSG, CategorySelectSG
from app.bot.utils.files import FileCredentials
from app.core.domain.models.file import FileId
from app.core.domain.models.user import User
from app.core.interfaces.usecase.file import FileUsecase


async def _process_new_title(_, __, manager: DialogManager, title: str):
    file_id: FileId = manager.start_data["file_id"]
    file_service: FileUsecase = manager.middleware_data["file_service"]
    user: User = manager.middleware_data[USER_KEY]

    await file_service.update_title(file_id, title, user.id)
    await manager.switch_to(FileEditSG.main)


async def _process_reload_file(m: Message, _: MessageInput, manager: DialogManager):
    cred = FileCredentials.from_message(m)
    file_id: int = manager.start_data["file_id"]
    file_service = manager.middleware_data["file_service"]
    user: User = manager.middleware_data[USER_KEY]

    await file_service.reload_file(file_id, cred.to_reload_dto(), user.id)
    await manager.switch_to(FileEditSG.main)


async def _on_start(start_data: dict | Any, manager: DialogManager):
    file_id = start_data["file_id"]
    if not manager.dialog_data.get("file_id"):
        manager.dialog_data["file_id"] = file_id

    if file_id is None:
        raise Exception("not provided file id")


async def _process_result(_, result: Any, manager: DialogManager):
    if not result or not isinstance(result, dict):
        return

    category_id = result.get("category_id")
    if category_id is None:
        return

    file_service: FileUsecase = manager.middleware_data.get("file_service")
    file_id: FileId = manager.start_data.get("file_id")
    user: User = manager.middleware_data[USER_KEY]

    await file_service.set_category(file_id, category_id, user.id)


async def _set_category_getter(dialog_manager: DialogManager, **_):
    file_id: int = dialog_manager.start_data["file_id"]
    return dict(file_id=file_id)


file_edit_dialog = Dialog(
    Window(
        Const("Выберите пункт"),
        Column(
            SwitchTo(
                Const("📝 Изменить название"),
                id="file_edit_title",
                state=FileEditSG.edit_title
            ),
            StartWithData(
                Const("🗂 Изменить категорию"),
                id="file_edit_c",
                state=CategorySelectSG.start,
                getter=_set_category_getter
            ),
            SwitchTo(
                Const("🔄 Перезагрузить файл"),
                id="file_edit_reload",
                state=FileEditSG.reload_file
            ),
            Cancel(CLOSE_TEXT),
        ),
        state=FileEditSG.main,
    ),
    Window(
        Const("Введите новое название"),
        TextInput(
            id="new__title",
            on_success=_process_new_title
        ),
        BackTo(FileEditSG.main, CANCEL_TEXT),
        state=FileEditSG.edit_title,
    ),

    Window(
        Const("Отправьте новый файл"),
        MessageInput(
            _process_reload_file,
            filter=MediaFilter()
        ),
        BackTo(FileEditSG.main, CANCEL_TEXT),
        state=FileEditSG.reload_file,
    ),
    on_process_result=_process_result,
    on_start=_on_start,
)
