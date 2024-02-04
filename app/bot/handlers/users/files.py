from aiogram import Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from app.bot.filters.media import MediaFilter
from app.bot.filters.via_self import ViaSelfRestrict
from app.bot.handlers.dialogs import execute
from app.bot.states.dialogs import ALLOWED_STATES
from app.bot.services import FileUploader
from app.core.interfaces.usecase import FileUsecase

router = Router()


@router.message(Command("list"))
async def command_list(msg: Message, dialog_manager: DialogManager):  # noqa
    del msg  # unused
    await execute.file_list(dialog_manager)


@router.message(MediaFilter(), ViaSelfRestrict(), StateFilter(None))
async def process_upload_file(msg: Message, file_service: FileUsecase, dialog_manager: DialogManager):
    # I don't have idea how get dialog_manager in filter
    # therefore will filter this and skip handler
    if dialog_manager.has_context():
        state = dialog_manager.current_context().state
        if state not in ALLOWED_STATES:
            raise SkipHandler

    uploader = FileUploader(file_service)
    file = await uploader.upload(msg)
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
