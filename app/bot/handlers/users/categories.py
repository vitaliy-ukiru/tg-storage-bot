from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nContext

from app.bot.handlers.dialogs import execute

router = Router(name="categories")


@router.message(Command("category"))
async def category_cmd(msg: Message, command: CommandObject, dialog_manager: DialogManager,
                       i18n: I18nContext):
    args = command.args
    if args is None:
        await msg.answer(i18n.get('missed-category-id-hint'))
        return
    try:
        category_id = int(args)
    except ValueError:
        await msg.answer(i18n.get('invalid-category-id-hint'))
    else:
        await execute.category_edit(dialog_manager, category_id)


@router.message(Command("create_category"))
async def create_category(msg: Message, dialog_manager: DialogManager):
    await execute.category_create(dialog_manager)
