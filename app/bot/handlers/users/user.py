from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.bot.handlers.dialogs import execute

router = Router()


@router.message(Command("locale"))
async def process_change_locale(m: Message, dialog_manager: DialogManager):
    await execute.change_locale(dialog_manager)


@router.message(Command("/stop"))
async def _stop_any(m: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.reset_stack(remove_keyboard=True)
    await state.clear()
    await m.answer("forced stop")
