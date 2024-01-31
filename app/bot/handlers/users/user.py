from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.bot.handlers.dialogs import execute

router = Router()


@router.message(Command("locale"))
async def process_change_locale(m: Message, dialog_manager: DialogManager):
    await execute.change_locale(dialog_manager)
