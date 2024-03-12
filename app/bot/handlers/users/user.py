from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from app.bot.handlers.dialogs import execute

router = Router()

HELP_TEXT = "help-text"
SWITCH_INLINE_BTN = "inline-mode-btn"


@router.message(Command("start"))
@router.message(Command("help"))
async def start_cmd(m: Message, i18n: I18nContext):
    await m.answer(
        text=i18n.get(HELP_TEXT),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=i18n.get(SWITCH_INLINE_BTN),
                switch_inline_query="",
            )]
        ])
    )


@router.message(Command("locale"))
async def process_change_locale(m: Message, dialog_manager: DialogManager):
    await execute.change_locale(dialog_manager)


@router.message(Command("/stop"))
async def _stop_any(m: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.reset_stack(remove_keyboard=True)
    await state.clear()
    await m.answer("forced stop")


@router.message(Command("menu"))
async def _start_menu(m: Message, dialog_manager: DialogManager):
    await execute.user_menu(dialog_manager)
