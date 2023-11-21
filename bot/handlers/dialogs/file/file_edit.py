from typing import Any, cast

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, Start, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Const

from bot.filters.media import MediaFilter
from bot.handlers.dialogs.back import BackTo
from bot.handlers.dialogs.category import SelectSG
from bot.handlers.dialogs.start_data import StartWithData
from bot.utils.files import FileCredentials
from core.domain.category import CategoryUseCase
from core.domain.file.service import FileUseCase


class EditSG(StatesGroup):
    main = State()
    edit_title = State()
    reload_file = State()


async def _process_new_title(m: Message, _: MessageInput, manager: DialogManager):
    title = m.text
    file_id: int = manager.start_data["file_id"]
    file_service = manager.middleware_data["file_service"]
    await file_service.update_title(file_id, title)
    await manager.switch_to(EditSG.main)


async def _process_reload_file(m: Message, _: MessageInput, manager: DialogManager):
    cred = FileCredentials.from_message(m)
    file_id: int = manager.start_data["file_id"]
    file_service = manager.middleware_data["file_service"]
    await file_service.reload_file(file_id, cred.to_reload_dto())
    await manager.switch_to(EditSG.main)


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

    file_service = cast(FileUseCase, manager.middleware_data.get("file_service"))
    category_service = cast(CategoryUseCase, manager.middleware_data.get("category_service"))
    category = await category_service.get_category(category_id)

    file_id = manager.start_data.get("file_id")
    await file_service.set_category(file_id, category)


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
                state=EditSG.edit_title
            ),
            StartWithData(
                Const("Изменить категорию"),
                id="file_edit_c",
                state=SelectSG.start,
                getter=_set_category_getter
            ),
            SwitchTo(
                Const("Перезагрузить файл"),
                id="file_edit_reload",
                state=EditSG.reload_file
            ),
            Cancel(),
        ),
        state=EditSG.main,
    ),
    Window(
        Const("Введите новое название"),
        MessageInput(
            _process_new_title
        ),
        BackTo(EditSG.main),
        state=EditSG.edit_title,
    ),

    Window(
        Const("Отправьте новый файл"),
        MessageInput(
            _process_reload_file,
            filter=MediaFilter()
        ),
        BackTo(EditSG.main),
        state=EditSG.reload_file,
    ),
    on_process_result=_process_result,
    on_start=_on_start

)
