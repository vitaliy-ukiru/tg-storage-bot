from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.bot.filters.media import MediaFilter
from app.bot.handlers.dialogs import execute
from app.bot.utils.uploader import FileUploader

router = Router()
@router.message(Command("list"))
async def command_list(msg: Message, dialog_manager: DialogManager):
    del msg # unused
    await execute.file_list(dialog_manager, mode=StartMode.RESET_STACK)

@router.message(MediaFilter(), StateFilter(None))
async def process_upload_file(msg: Message, uploader: FileUploader, dialog_manager: DialogManager):
    if dialog_manager.has_context():
        return

    file = await uploader.upload(msg)
    await execute.file_view(dialog_manager, file.id)


@router.message(Command("file"))
async def file_cmd(msg: Message, command: CommandObject, dialog_manager: DialogManager):
    args = command.args
    try:
        file_id = int(args)
    except Exception as _:
        await msg.answer("invalid file_id")
        return
    await execute.file_view(dialog_manager, file_id, mode=StartMode.RESET_STACK)
