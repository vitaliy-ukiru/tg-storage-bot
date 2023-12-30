from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.bot.filters.media import MediaFilter
from app.bot.handlers.dialogs import execute
from app.bot.states.dialogs import CategoryCreateSG
from app.bot.utils.uploader import FileUploader

router = Router(name="categories")
@router.message(Command("cat"))
async def category_cmd(msg: Message, command: CommandObject, dialog_manager: DialogManager):
    args = command.args
    try:
        category_id = int(args)
    except Exception as _:
        await msg.answer("invalid category_id")
        return
    await execute.category_edit(dialog_manager, category_id, mode=StartMode.RESET_STACK)

@router.message(Command("create_category"))
async def create_category(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(CategoryCreateSG.input_title)