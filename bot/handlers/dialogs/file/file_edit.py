from typing import Any

from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Const

from bot.filters.media import MediaFilter
from bot.handlers.dialogs.custom.back import BackTo
from bot.handlers.dialogs.start_data import StartWithData
from bot.middlewares.user_manager import USER_KEY
from bot.states.dialogs import FileEditSG, CategorySelectSG
from bot.utils.files import FileCredentials
from core.domain.models.file import FileId
from core.domain.models.user import User
from core.domain.services.file import FileUsecase


async def _process_new_title(m: Message, _: MessageInput, manager: DialogManager):
    title = m.text
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

    await file_service.reload_file(file_id, cred.to_reload_dto(), user)
    await manager.switch_to(FileEditSG.main)


async def _on_start(start_data: dict | Any, manager: DialogManager):
    file_id = start_data["file_id"]
    if not manager.dialog_data.get("file_id"):
        manager.dialog_data["file_id"] = file_id

    if file_id is None:
        raise Exception("not provided file id")


async def _process_result(start_data: Data, result: Any, manager: DialogManager):
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
                Const("Изменить название"),
                id="file_edit_title",
                state=FileEditSG.edit_title
            ),
            StartWithData(
                Const("Изменить категорию"),
                id="file_edit_c",
                state=CategorySelectSG.start,
                getter=_set_category_getter
            ),
            SwitchTo(
                Const("Перезагрузить файл"),
                id="file_edit_reload",
                state=FileEditSG.reload_file
            ),
            Cancel(),
        ),
        state=FileEditSG.main,
    ),
    Window(
        Const("Введите новое название"),
        MessageInput(
            _process_new_title
        ),
        BackTo(FileEditSG.main),
        state=FileEditSG.edit_title,
    ),

    Window(
        Const("Отправьте новый файл"),
        MessageInput(
            _process_reload_file,
            filter=MediaFilter()
        ),
        BackTo(FileEditSG.main),
        state=FileEditSG.reload_file,
    ),
    on_process_result=_process_result,
    on_start=_on_start,
)
