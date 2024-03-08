from aiogram import Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from app.bot.filters import MediaFilter, ViaSelfRestrict
from app.bot.handlers.dialogs import execute
from app.bot.services import FileUploader
from app.bot.states.dialogs import ALLOWED_STATES, CategoryEditSG
from app.core.domain.exceptions.file import FileAlreadyExists
from app.core.domain.models.category import CategoryId
from app.core.interfaces.usecase import FileUsecase

router = Router()


@router.message(Command("list"))
async def command_list(msg: Message, dialog_manager: DialogManager):  # noqa
    del msg  # unused
    await execute.file_list(dialog_manager)


@router.message(MediaFilter(), ViaSelfRestrict(), StateFilter(None))
async def process_upload_file(
    msg: Message,
    file_service: FileUsecase,
    dialog_manager: DialogManager,
    i18n: I18nContext,
):
    category_id: CategoryId | None = None
    # I don't have idea how get dialog_manager in filter
    # therefore will filter this and skip handler
    if dialog_manager.has_context():
        state = dialog_manager.current_context().state
        if state not in ALLOWED_STATES:
            raise SkipHandler

        if state == CategoryEditSG.main:
            category_id = dialog_manager.dialog_data["category_id"]

    uploader = FileUploader(file_service)
    try:

        file = await uploader.upload(msg, category_id)
    except FileAlreadyExists:
        await msg.answer(i18n.get("file-already-exists"))
    else:
        await execute.file_view(dialog_manager, file.id)


@router.message(Command("file"))
async def file_cmd(
    msg: Message,
    command: CommandObject,
    dialog_manager: DialogManager,
    i18n: I18nContext
):
    args = command.args
    if args is None:
        await msg.answer(i18n.get('missed-file-id-hint'))
        return
    try:
        file_id = int(args)
    except ValueError as _:
        await msg.answer(i18n.get('invalid-file-id-hint'))
    else:
        await execute.file_view(dialog_manager, file_id)
