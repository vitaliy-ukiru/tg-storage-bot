import logging
from contextlib import suppress

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, ReplyKeyboardRemove, Update
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent
from aiogram_i18n import I18nContext

from app.core.domain.exceptions.category import CategoryNotFound, CategoryAccessDenied
from app.core.domain.exceptions.file import FileNotFound, FileAccessDenied

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


@router.errors(ExceptionTypeFilter(FileNotFound))
async def _on_file_not_found(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    i18n: I18nContext
):
    await _send_error_info(event.update, dialog_manager, i18n, "file-not-found")


@router.errors(ExceptionTypeFilter(CategoryNotFound))
async def _on_category_not_found(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    i18n: I18nContext
):
    await _send_error_info(event.update, dialog_manager, i18n, "category-not-found")


@router.errors(ExceptionTypeFilter(FileAccessDenied))
async def _on_file_access_denied(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    i18n: I18nContext
):
    await _send_error_info(event.update, dialog_manager, i18n, "file-access-denied")


@router.errors(ExceptionTypeFilter(CategoryAccessDenied))
async def _on_category_access_denied(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    i18n: I18nContext
):
    await _send_error_info(event.update, dialog_manager, i18n, "category-access-denied")


async def _send_error_info(
    update: Update,
    dialog_manager: DialogManager,
    i18n: I18nContext,
    key: str
):
    if dialog_manager.has_context():
        await dialog_manager.done()
    text = i18n.get(key)
    if update.message:
        await update.message.answer(text)
    elif update.callback_query:
        await update.callback_query.message.answer(text)
