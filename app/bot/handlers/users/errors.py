import logging
from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent

router = Router()


@router.errors(ExceptionTypeFilter(UnknownIntent))
async def _on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Reset dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer("Unknown intent. Restarting")
        if event.update.callback_query.message:
            with suppress(TelegramBadRequest):
                await event.update.callback_query.message.delete()

    elif event.update.message:
        await event.update.message.answer(
            "Unknown intent. Restarting",
            reply_markup=ReplyKeyboardRemove(),
        )

    await dialog_manager.reset_stack(remove_keyboard=True)