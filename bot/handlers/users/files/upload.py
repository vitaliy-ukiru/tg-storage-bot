from aiogram import Router
from aiogram.types import Message

from bot.filters.media import MediaFilter
from bot.ui.file import FileView
from bot.utils.uploader import FileUploader

router = Router(name="base-upload-files")


@router.message(MediaFilter(), StateFilter(None),)
async def process_upload_file(msg: Message, uploader: FileUploader, dialog_manager: DialogManager):
    if dialog_manager.current_context():
        return

    file = await uploader.upload(msg)
    await dialog_manager.start(ViewSG.main, dict(file_id=file.id))

@router.message(Command("file"))
async def file_cmd(msg: Message, command: CommandObject, dialog_manager: DialogManager):
    args = command.args
    try:
        file_id = int(args)
    except:
        await msg.answer("invalid file_id")
        return
    await dialog_manager.start(ViewSG.main, dict(file_id=file_id), mode=StartMode.RESET_STACK)

