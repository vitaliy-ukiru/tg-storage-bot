from aiogram import Router, Bot
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.enums import ReactionTypeType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, MessageReactionUpdated
from aiogram_dialog import DialogManager, BgManagerFactory
from aiogram_i18n import I18nContext

from app.bot.handlers.dialogs import execute
from app.bot.handlers.dialogs.category.edit_category import (
    MARKER_FROM_REACTION,
    DELETE_MARKER,
    MARKER_MESSAGE_ID
)

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
async def create_category(_: Message, dialog_manager: DialogManager):
    await execute.category_create(dialog_manager)


async def _get_custom_emoji(bot: Bot, custom_emoji_id: str):
    stickers = await bot.get_custom_emoji_stickers([custom_emoji_id])
    sticker = stickers[0]
    return sticker.emoji


async def filter_new_reactions(event: MessageReactionUpdated) -> bool:
    return len(event.new_reaction) == 1


async def filter_old_reactions(event: MessageReactionUpdated) -> bool:
    return event.old_reaction and not event.new_reaction


async def _check_is_category_edit(
    event: MessageReactionUpdated,
    bot: Bot,
    i18n: I18nContext,
):
    try:
        msg = await bot.edit_message_reply_markup(event.chat.id, event.message_id)
    except TelegramBadRequest:
        return False

    if not msg.from_user.is_bot or msg.from_user.id != bot.id:
        return False

    prefix = i18n.get("category-edit-tag")
    return msg.text.startswith(prefix)


@router.message_reaction(filter_new_reactions)
async def _set_marker_by_reaction(
    event: MessageReactionUpdated,
    dialog_bg_factory: BgManagerFactory,
    bot: Bot,
    i18n: I18nContext,
):
    if not await _check_is_category_edit(event, bot, i18n):
        raise SkipHandler()

    reaction = event.new_reaction[0]
    if reaction.type == ReactionTypeType.CUSTOM_EMOJI:
        emoji = await _get_custom_emoji(bot, reaction.custom_emoji_id)
        if not emoji:
            return
    else:
        emoji = reaction.emoji

    manager = dialog_bg_factory.bg(bot, event.user.id, event.chat.id)
    await manager.update(data={
        MARKER_FROM_REACTION: emoji,
        MARKER_MESSAGE_ID: event.message_id
    })


@router.message_reaction(filter_old_reactions)
async def _delete_marker_by_reaction(
    event: MessageReactionUpdated,
    dialog_bg_factory: BgManagerFactory,
    bot: Bot,
    i18n: I18nContext,
):
    if not await _check_is_category_edit(event, bot, i18n):
        raise SkipHandler()

    manager = dialog_bg_factory.bg(bot, event.user.id, event.chat.id)
    await manager.update(data={
        MARKER_FROM_REACTION: DELETE_MARKER,
        MARKER_MESSAGE_ID: event.message_id
    })
