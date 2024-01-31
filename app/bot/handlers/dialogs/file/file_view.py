from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Button, Back
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format
from aiogram_i18n import I18nContext
from magic_filter import F

from app.bot.middlewares.user_manager import USER_KEY
from app.bot.states.dialogs import FileViewSG, FileEditSG
from app.bot.utils.file_type_i18n import locale_file_type
from app.bot.utils.files import content_type_from_category
from app.bot.widgets import StartWithData
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import TemplateProxy, Topic, CloseI18n
from app.bot.widgets.i18n.file_title import FileTitle
from app.bot.widgets.i18n.template import I18N_KEY
from app.core.domain.models.file import FileId
from app.core.domain.models.user import User
from app.core.interfaces.usecase.file import FileUsecase

tl_file_view = TemplateProxy('file-view')


async def _process_delete_file(call: CallbackQuery, _: Button, manager: DialogManager):
    file_id: FileId = manager.start_data["file_id"]
    file_service: FileUsecase = manager.middleware_data["file_service"]
    user: User = manager.middleware_data[USER_KEY]
    i18n: I18nContext = manager.middleware_data[I18N_KEY]

    await file_service.delete_file(file_id, user.id)
    await call.message.edit_text(i18n.get(str(tl_file_view.removed)))  # type: ignore
    await manager.done()


async def _view_getter(dialog_manager: DialogManager, file_service: FileUsecase, i18n: I18nContext, **_):
    file_id: FileId = dialog_manager.start_data["file_id"]
    user: User = dialog_manager.middleware_data[USER_KEY]

    file = await file_service.get_file(file_id, user.id)
    category_name = None
    if file.category is not None:
        category_name = file.category.title

    return dict(
        file=file,
        file_type_name=locale_file_type(file.type, i18n),
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
    content_type = content_type_from_category(file.type.category)
    media = MediaAttachment(content_type, file_id=MediaId(file.remote_file_id))
    return dict(file_media=media, file_id=file_id)


async def _process_back_to_menu_click(__: CallbackQuery, _: Button, manager: DialogManager):
    file_id: int = manager.start_data["file_id"]
    await manager.start(FileViewSG.main, dict(file_id=file_id), mode=StartMode.RESET_STACK)


file_view_dialog = Dialog(
    Window(
        Topic(
            tl_file_view.topic.title(),
            FileTitle(
                Format("{file.title}"),
                F["file"].id,
                F["file"].title
            )
        ),
        Topic(
            tl_file_view.topic.title(),
            Format("{file_category}"),
            when="file_category"
        ),
        Topic(
            tl_file_view.topic.type(),
            Format("{file_type_name}")
        ),
        Topic(
            tl_file_view.topic.created(),
            Format("{upload_time}")
        ),
        Column(
            SwitchTo(
                Emoji("📥", tl_file_view.btn.send()),
                id="send_file",
                state=FileViewSG.send_file,
            ),
            StartWithData(
                Emoji("✏️", tl_file_view.btn.edit()),
                id="edit_file",
                state=FileEditSG.main,
                getter=_file_edit_getter
            ),
            Button(
                Emoji("❌", tl_file_view.btn.delete()),
                id="delete_file",
                on_click=_process_delete_file
            )
        ),
        CloseI18n(),
        getter=_view_getter,
        state=FileViewSG.main,
    ),
    Window(
        DynamicMedia("file_media"),
        Back(
            tl_file_view.btn.menu(),
            id="show_menu",
        ),
        getter=_media_getter,
        state=FileViewSG.send_file,
    )
)
