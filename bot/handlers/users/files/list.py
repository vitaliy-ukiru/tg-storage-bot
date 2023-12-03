from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.handlers.dialogs import execute

router = Router()

@router.message(Command("list"))
async def command_list(msg: Message, dialog_manager: DialogManager):
    await execute.file_list(dialog_manager, mode=StartMode.RESET_STACK)