from aiogram import Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.bot.filters.media import MediaFilter
from app.bot.handlers.dialogs import execute
from app.bot.states.dialogs import ALLOWED_STATES
from app.bot.utils.uploader import FileUploader

router = Router()
@router.message(Command("list"))
async def command_list(msg: Message, dialog_manager: DialogManager):
    del msg # unused
    await execute.file_list(dialog_manager, mode=StartMode.RESET_STACK)


@router.message(MediaFilter(), StateFilter(None))
async def process_upload_file(msg: Message, uploader: FileUploader, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    if ctx is not None:
        state = ctx.state
        if state not in ALLOWED_STATES:
            raise SkipHandler

    file = await uploader.upload(msg)
    await execute.file_view(
        dialog_manager,
        file.id,
        mode=StartMode.RESET_STACK,
    )


@router.message(Command("file"))
async def file_cmd(msg: Message, command: CommandObject, dialog_manager: DialogManager):
    args = command.args
    try:
        file_id = int(args)
    except ValueError as _:
        await msg.answer("invalid file_id")
        return
    await execute.file_view(dialog_manager, file_id, mode=StartMode.RESET_STACK)
