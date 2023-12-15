from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Button, Cancel, Back
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from app.bot.states.dialogs import FileViewSG, FileEditSG
from app.bot.utils.file_type_str import get_file_type_name
from app.core.domain.models.file import FileId
from app.core.domain.models.user import User
from app.core.interfaces.usecase.file import FileUsecase

from app.bot.middlewares.user_manager import USER_KEY
from app.bot.utils.files import content_type_from_file
from app.bot.handlers.dialogs.custom.start_data import StartWithData


async def _process_delete_file(call: CallbackQuery, _: Button, manager: DialogManager):
    file_id: FileId = manager.start_data["file_id"]
    file_service: FileUsecase = manager.middleware_data["file_service"]
    user: User = manager.middleware_data[USER_KEY]

    await file_service.delete_file(file_id, user.id)
    await call.message.edit_text("Файл удалён")
    await manager.done()


async def _view_getter(dialog_manager: DialogManager, file_service: FileUsecase, **_):
    file_id: FileId = dialog_manager.start_data["file_id"]
    user: User = dialog_manager.middleware_data[USER_KEY]

    file = await file_service.get_file(file_id, user.id)
    category_name = None
    if file.category is not None:
        category_name = file.category.title

    return dict(
        file_id=file.id,
        file_title=file.name,
        file_type=file.type,
        file_type_name=get_file_type_name(file.type),
        file_category=category_name,
        upload_time=file.created_at.strftime("%Y-%m-%d %H:%M:%S %Z")
    )


async def _file_edit_getter(dialog_manager: DialogManager, **_):
    file_id: int = dialog_manager.start_data["file_id"]
    return dict(file_id=file_id)


async def _media_getter(dialog_manager: DialogManager, file_service: FileUsecase, **_):
    file_id: FileId = dialog_manager.start_data["file_id"]
    user: User = dialog_manager.middleware_data[USER_KEY]

    file = await file_service.get_file(file_id, user.id)
    content_type = content_type_from_file(file.type)
    media = MediaAttachment(content_type, file_id=MediaId(file.remote_file_id))
    return dict(file_media=media, file_id=file_id)


async def _process_back_to_menu_click(__: CallbackQuery, _: Button, manager: DialogManager):
    file_id: int = manager.start_data["file_id"]
    await manager.start(FileViewSG.main, dict(file_id=file_id), mode=StartMode.RESET_STACK)


file_view_dialog = Dialog(
    Window(
        Format("Название: {file_title}"),
        Format("Категория: {file_category}", when=F["file_category"]),
        Format("Тип: {file_type_name}"),
        Format("Дата загрузки: {upload_time}"),
        Column(
            SwitchTo(
                Const("📥 Отправить файл"),
                id="send_file",
                state=FileViewSG.send_file,
            ),
            StartWithData(
                Const("✏️ Редактировать файл"),
                id="edit_file",
                state=FileEditSG.main,
                getter=_file_edit_getter
            ),
            Button(
                Const("❌ Удалить файл"),
                id="delete_file",
                on_click=_process_delete_file
            )
        ),
        Cancel(Const("Закрыть")),
        getter=_view_getter,
        state=FileViewSG.main,
    ),
    Window(
        DynamicMedia("file_media"),
        Back(
            Const("Меню"),
            id="show_menu",
        ),
        getter=_media_getter,
        state=FileViewSG.send_file,
    )
)
