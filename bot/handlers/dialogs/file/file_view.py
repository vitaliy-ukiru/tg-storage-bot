from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Column, Start, SwitchTo, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.handlers.dialogs.back import BackTo
from .file_edit import EditSG
from bot.utils.files import content_type_from_file
from core.domain.file.service import FileUseCase
from ..start_data import StartWithData


# async def _(m: Message, _: MessageInput, manager: DialogManager,
#             file_service: FileUseCase):
#         pass

async def _process_delete_file(call: CallbackQuery, _: Button, manager: DialogManager):
    file_id: int = manager.start_data["file_id"]
    file_service = manager.middleware_data["file_service"]
    await file_service.delete_file(file_id)
    await call.message.edit_text("Файл удалён")
    await manager.done()


async def _view_getter(dialog_manager: DialogManager, file_service: FileUseCase, **_):
    file_id: int = dialog_manager.start_data["file_id"]
    file = await file_service.get_file_by_id(file_id)
    category_name = None
    if file.category is not None:
        category_name = file.category.title

    return dict(
        file_id=file.id,
        file_title=file.title,
        file_type=file.type,
        file_category=category_name,
        upload_time=file.created_at.strftime("%Y-%m-%d %H:%M:%S %Z")
    )

async def _file_edit_getter(dialog_manager: DialogManager, **_):
    file_id: int = dialog_manager.start_data["file_id"]
    return dict(file_id=file_id)
async def _media_getter(dialog_manager: DialogManager, file_service: FileUseCase, **_):
    file_id: int = dialog_manager.start_data["file_id"]
    file = await file_service.get_file_by_id(file_id)
    content_type = content_type_from_file(file.type)
    media = MediaAttachment(content_type, file_id=MediaId(file.remote_file_id))
    return dict(file_media=media, file_id=file_id)

async def _process_back_to_menu_click(__: CallbackQuery, _: Button, manager: DialogManager):
    file_id: int = manager.start_data["file_id"]
    await manager.start(ViewSG.main, dict(file_id=file_id), mode=StartMode.RESET_STACK)

class ViewSG(StatesGroup):
    main = State()
    send_file = State()


file_view_dialog = Dialog(
    Window(
        Format("Название: {file_title}"),
        Format("Категория: {file_category}", when=F["file_category"]),
        Format("Тип: {file_type}"),
        Format("Дата загрузки: {upload_time}"),
        Column(
            SwitchTo(
                Const("Отправить файл"),
                id="send_file",
                state=ViewSG.send_file,
            ),
            StartWithData(
                Const("Редактировать файл"),
                id="edit_file",
                state=EditSG.main,
                getter=_file_edit_getter
            ),
            Button(
                Const("Удалить файл"),
                id="delete_file",
                on_click=_process_delete_file
            )
        ),
        getter=_view_getter,
        state=ViewSG.main,
    ),
    Window(
        DynamicMedia("file_media"),
        Button(
            Const("Меню"),
            id="show_menu",
            on_click=_process_back_to_menu_click,
        ),
        getter=_media_getter,
        state=ViewSG.send_file,
    )
)
