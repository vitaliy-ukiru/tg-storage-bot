from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, Data, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Checkbox, ManagedCheckbox, Select, Column
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from app.bot.filters import MediaFilter
from app.bot.handlers.dialogs import execute
from app.bot.middlewares.user_manager import ACCESS_CONTROLLER_KEY
from app.bot.services import FileUploader
from app.bot.states.dialogs import UploadFileSG, CategoryFindSG
from app.bot.widgets import Emoji
from app.bot.widgets.i18n import Template, CloseI18n, TemplateProxy, Topic, FileTitle
from app.core.domain.exceptions.file import FileAlreadyExists
from app.core.interfaces.access import AccessController
from app.core.interfaces.usecase import CategoryUsecase, FileUsecase

TL = TemplateProxy("file", "upload")

ALREADY_EXISTS_KEY = "err_already_exists"
MULTIPLE_UPLOAD_ID = "multiple_upload"
FILES_HISTORY_LIST = "files_list"


async def _on_send_file(m: Message, _, manager: DialogManager):
    category_id = manager.dialog_data.get("category_id")
    file_service = manager.middleware_data["file_service"]
    ac = manager.middleware_data[ACCESS_CONTROLLER_KEY]

    multiple_upload_checkbox: ManagedCheckbox = manager.find(MULTIPLE_UPLOAD_ID)

    uploader = FileUploader(file_service)
    try:
        file = await uploader.upload(m, ac, category_id)
    except FileAlreadyExists:
        manager.dialog_data[ALREADY_EXISTS_KEY] = True
        return

    if multiple_upload_checkbox.is_checked():
        files = manager.dialog_data.setdefault(FILES_HISTORY_LIST, [])
        files.append(file.id)
        return

    await execute.file_view(manager, file.id, mode=StartMode.NORMAL)


async def _getter(
    dialog_manager: DialogManager,
    category_service: CategoryUsecase,
    file_service: FileUsecase,
    access_controller: AccessController,
    **_,
):
    category_id = dialog_manager.dialog_data.get("category_id")
    data = {
        ALREADY_EXISTS_KEY: dialog_manager.dialog_data.pop(ALREADY_EXISTS_KEY, False)
    }

    if category_id:
        category = await category_service.get_category(category_id, access_controller)
        data["category"] = category.title

    files_ids = dialog_manager.dialog_data.get(FILES_HISTORY_LIST)
    if files_ids:
        files = [
            await file_service.get_file(file_id, access_controller)

            for file_id in files_ids
        ]
        data["files"] = files

    return data


async def _on_process_result(start_data: Data, result, manager: DialogManager):
    if result:
        manager.dialog_data["category_id"] = result["category_id"]


async def _process_click_file(_, __, manager: DialogManager, item_id: int):
    await execute.file_view(manager, item_id, data=dict(opened_over=True), mode=StartMode.NORMAL)


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
                "allow_create": True,
            },
            state=CategoryFindSG.main,
        ),
        Checkbox(
            Emoji("✅", TL.multiple()),
            TL.multiple(),
            id=MULTIPLE_UPLOAD_ID,

        ),
        Column(
            Select(
                FileTitle(
                    Format("{item.title}"),
                    F["item"].id,
                    F["item"].title
                ),
                id="file_history",
                type_factory=int,
                on_click=_process_click_file,
                item_id_getter=lambda file: file.id,
                items="files",
                when="files",
            ),
        ),
        MessageInput(_on_send_file, filter=MediaFilter()),
        CloseI18n(),
        state=UploadFileSG.main,
        getter=_getter,
    ),
    on_process_result=_on_process_result
)
