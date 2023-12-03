from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.filters.media import MediaFilter
from bot.handlers.dialogs import execute
from bot.utils.uploader import FileUploader

router = Router(name="base-upload-files")


@router.message(MediaFilter(), StateFilter(None), )
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
