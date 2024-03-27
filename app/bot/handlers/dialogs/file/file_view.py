from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Column, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format
from aiogram_i18n import I18nContext
from magic_filter import F

from app.bot.middlewares.user_manager import ISSUER_KEY
from app.bot.services import content_type_from_category
from app.bot.states.dialogs import FileViewSG, FileEditSG
from app.bot.utils import locale_file_type
from app.bot.widgets import StartWithData, Emoji
from app.bot.widgets.i18n import TemplateProxy, Topic, CloseI18n, FileTitle, I18N_KEY
from app.core.domain.models.file import FileId
from app.core.interfaces.usecase import FileUsecase

tl_file_view = TemplateProxy('file-view')


async def _process_delete_file(call: CallbackQuery, _: Button, manager: DialogManager):
    file_id: FileId = manager.start_data["file_id"]
    file_service: FileUsecase = manager.middleware_data["file_service"]
    issuer = manager.middleware_data[ISSUER_KEY]
    i18n: I18nContext = manager.middleware_data[I18N_KEY]

    await file_service.delete_file(file_id, issuer)
    await call.message.edit_caption(i18n.get(str(tl_file_view.removed)))  # type: ignore
    await manager.done()


async def _view_getter(dialog_manager: DialogManager, file_service: FileUsecase, i18n: I18nContext, **_):
    file_id: FileId = dialog_manager.start_data["file_id"]
    issuer = dialog_manager.middleware_data[ISSUER_KEY]

    file = await file_service.get_file(file_id, issuer)
    category_name = None
    if file.category is not None:
        category_name = file.category.title

    content_type = content_type_from_category(file.type.category)
    media = MediaAttachment(content_type, file_id=MediaId(file.remote_file_id))

    return dict(
        file=file,
        file_type_name=locale_file_type(file.type, i18n),
        file_category=category_name,
        file_media=media,
    )


async def _file_edit_getter(dialog_manager: DialogManager, **_):
    file_id: int = dialog_manager.start_data["file_id"]
    return dict(file_id=file_id)


file_view_dialog = Dialog(
    Window(
        DynamicMedia("file_media"),
        Topic(
            tl_file_view.topic.title(),
            FileTitle(
                Format("{file.title}"),
                F["file"].id,
                F["file"].title
            )
        ),
        Topic(
            tl_file_view.topic.category(),
            Format("{file_category}"),
            when="file_category"
        ),
        Topic(
            tl_file_view.topic.type(),
            Format("{file_type_name}")
        ),
        tl_file_view.topic.created(
            getter=lambda data: dict(upload_time=data["file"].created_at)
        ),
        Column(
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
)
