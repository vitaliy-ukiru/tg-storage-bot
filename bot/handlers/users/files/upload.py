from aiogram import Router
from aiogram.types import Message

from bot.filters.media import MediaFilter
from bot.ui.file import FileView
from bot.utils.uploader import FileUploader

router = Router(name="base-upload-files")


@router.message(MediaFilter())
async def process_upload_file(msg: Message, uploader: FileUploader):
    file = await uploader.upload_by_content_type(msg)
    view = FileView(file)
    await view.send(msg.bot, msg.chat.id)
