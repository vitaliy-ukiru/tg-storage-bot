from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, Data, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format

from app.bot.filters import MediaFilter
from app.bot.handlers.dialogs import execute
from app.bot.services import FileUploader
from app.bot.states.dialogs import UploadFileSG, CategoryFindSG
from app.bot.widgets.i18n import Template, CloseI18n, TemplateProxy, Topic
from app.core.domain.exceptions.file import FileAlreadyExists
from app.core.domain.models.user import User
from app.core.interfaces.usecase import CategoryUsecase

TL = TemplateProxy("file", "upload")

ALREADY_EXISTS_KEY = "err_already_exists"


async def _on_send_file(m: Message, _, manager: DialogManager):
    category_id = manager.dialog_data.get("category_id")
    file_service = manager.middleware_data["file_service"]

    uploader = FileUploader(file_service)
    try:
        file = await uploader.upload(m, category_id)
    except FileAlreadyExists:
        manager.dialog_data[ALREADY_EXISTS_KEY] = True
        return

    await execute.file_view(manager, file.id, mode=StartMode.NORMAL)


async def _getter(
    dialog_manager: DialogManager,
    category_service: CategoryUsecase,
    user: User,
    **_,
):
    category_id = dialog_manager.dialog_data.get("category_id")
    data = {
        ALREADY_EXISTS_KEY: dialog_manager.dialog_data.pop(ALREADY_EXISTS_KEY, False)
    }

    if category_id:
        category = await category_service.get_category(category_id, user.id)
        data["category"] = category.title

    return data


async def _on_process_result(start_data: Data, result, manager: DialogManager):
    if result:
        manager.dialog_data["category_id"] = result["category_id"]


file_upload_dialog = Dialog(
    Window(
        Topic(
            Template("common-category"),
            Format("{category}"),
            when="category",
        ),
        Template("file-already-exists", when=ALREADY_EXISTS_KEY),
        TL.send(),

        Start(
            TL.add.category(),
            id="add_category",
            data={
                "allowed_create": True,
            },
            state=CategoryFindSG.main,
        ),
        MessageInput(_on_send_file, filter=MediaFilter()),
        CloseI18n(),
        state=UploadFileSG.main,
        getter=_getter,
    ),
    on_process_result=_on_process_result
)
