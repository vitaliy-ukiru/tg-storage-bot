from typing import Optional

import emoji
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Group, Cancel, Row
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_i18n import I18nContext

from app.bot.states.dialogs import CategoryCreateSG
from app.bot.utils.optional_str import optional_str_factory
from app.bot.widgets.dao.base_dao import BaseDAO
from app.bot.widgets.dao.widgets import TextInputProp
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import CANCEL_TEXT, Topic, BackI18n, TL
from app.common.helpers import is_category_marker_valid
from app.core.domain.dto.category import CreateCategoryDTO
from app.core.domain.exceptions.category import InvalidCategoryMarker
from app.core.interfaces.usecase.category import CategoryUsecase

ID_INPUT_TITLE = "input_title"
ID_INPUT_DESC = "input_desc"
ID_INPUT_MARKER = "input_marker"

tl = TL.category.create


class CreateCategoryDAO(BaseDAO):
    title = TextInputProp[str](ID_INPUT_TITLE)
    desc = TextInputProp[str | None](ID_INPUT_DESC)
    marker = TextInputProp[str | None](ID_INPUT_MARKER)


async def _to_menu(_: Message, __, manager: DialogManager, ___: str):
    await manager.switch_to(CategoryCreateSG.menu_idle)


async def _on_marker_input(m: Message, __, manager: DialogManager, value: str):
    if not is_category_marker_valid(value):
        i18n: I18nContext = manager.middleware_data["i18n"]
        await m.answer(i18n.get("category-invalid-marker"))
        return

    await manager.switch_to(CategoryCreateSG.menu_idle)


async def menu_getter(dialog_manager: DialogManager, **_):
    dao = CreateCategoryDAO(dialog_manager)
    return dict(title=dao.title, desc=dao.desc, marker=dao.marker)


async def create_category(call: CallbackQuery, _: Button, manager: DialogManager):
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    dao = CreateCategoryDAO(manager)
    try:
        category = await category_service.save_category(CreateCategoryDTO(
            title=dao.title,
            desc=dao.desc,
            user_id=call.from_user.id,
            marker=dao.marker,
        ))
    except InvalidCategoryMarker:
        i18n: I18nContext = manager.middleware_data["i18n"]
        await call.answer(i18n.get("category-invalid-marker"), show_alert=True)
        return

    await manager.done(dict(category_id=category.id, category=category))


category_create_dialog = Dialog(
    Window(
        tl.input.title(),
        TextInput(id=ID_INPUT_TITLE, on_success=_to_menu),
        state=CategoryCreateSG.input_title,
    ),

    Window(
        Multi(
            Topic(
                TL.category.title(),
                Format("{title}")
            ),
            Topic(
                TL.category.desc(),
                Format("{desc}"),
                when="desc"
            ),
            Topic(
                TL.category.marker(),
                Format("{marker}"),
                when="marker"
            )
        ),
        Group(
            Row(
                SwitchTo(
                    Emoji("📝", tl.btn.title()),
                    id="edit_title",
                    state=CategoryCreateSG.input_title
                ),
                SwitchTo(
                    Emoji("📝", tl.btn.desc()),
                    id="edit_desc",
                    state=CategoryCreateSG.input_desc
                ),
                SwitchTo(
                    Emoji("🟢", tl.btn.marker()),
                    id="edit_marker",
                    state=CategoryCreateSG.input_marker,
                )
            ),
            Button(
                Emoji("✅", tl.btn.create()),
                id="create",
                on_click=create_category,
            ),
            Cancel(CANCEL_TEXT)
        ),
        getter=menu_getter,
        state=CategoryCreateSG.menu_idle,
    ),

    Window(
        tl.input.desc(),
        BackI18n(),
        TextInput[Optional[str]](
            id=ID_INPUT_DESC,
            type_factory=optional_str_factory,
            on_success=_to_menu
        ),
        state=CategoryCreateSG.input_desc
    ),
    Window(
        tl.input.marker(),
        BackI18n(),
        TextInput(
            id=ID_INPUT_MARKER,
            type_factory=optional_str_factory,
            on_success=_on_marker_input
        ),
        state=CategoryCreateSG.input_marker,
    )
)
