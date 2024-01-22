from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Group, Cancel, Row
from aiogram_dialog.widgets.text import Format, Multi

from app.bot.states.dialogs import CategoryCreateSG
from app.bot.utils.optional_str import optional_str_factory
from app.bot.widgets.dao.base_dao import BaseDAO
from app.bot.widgets.dao.widgets import TextInputProp
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import CANCEL_TEXT, LC, Template, Topic, BackI18n
from app.core.domain.dto.category import CreateCategoryDTO
from app.core.interfaces.usecase.category import CategoryUsecase

ID_INPUT_TITLE = "input_title"
ID_INPUT_DESC = "input_desc"

lc = LC.category.create


class CreateCategoryDAO(BaseDAO):
    title = TextInputProp[str](ID_INPUT_TITLE)
    desc = TextInputProp[str | None](ID_INPUT_DESC)


async def _to_menu(_: Message, __, manager: DialogManager, ___: str):
    await manager.switch_to(CategoryCreateSG.menu_idle)


async def menu_getter(dialog_manager: DialogManager, **_):
    dao = CreateCategoryDAO(dialog_manager)
    return dict(title=dao.title, desc=dao.desc)


async def create_category(call: CallbackQuery, _: Button, manager: DialogManager):
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    dao = CreateCategoryDAO(manager)
    category = await category_service.save_category(CreateCategoryDTO(
        title=dao.title,
        desc=dao.desc,
        user_id=call.from_user.id
    ))

    await manager.done(dict(category_id=category.id, category=category))


category_create_dialog = Dialog(
    Window(
        Template(lc.input.title),
        TextInput(id=ID_INPUT_TITLE, on_success=_to_menu),
        state=CategoryCreateSG.input_title,
    ),

    Window(
        Multi(
            Topic(
                LC.category.title,
                Format("{title}")
            ),
            Topic(
                LC.category.desc,
                Format("{desc}"),
                when="desc"
            )
        ),
        Group(
            Row(
                SwitchTo(
                    Emoji("📝", Template(lc.btn.title)),
                    id="edit_title",
                    state=CategoryCreateSG.input_title
                ),
                SwitchTo(
                    Emoji("📝", Template(lc.btn.desc)),
                    id="edit_desc",
                    state=CategoryCreateSG.input_desc
                ),
            ),
            Button(
                Emoji("✅", Template(lc.btn.create)),
                id="create",
                on_click=create_category,
            ),
            Cancel(CANCEL_TEXT)
        ),
        getter=menu_getter,
        state=CategoryCreateSG.menu_idle,
    ),

    Window(
        Template(lc.input.desc),
        BackI18n(),
        TextInput[Optional[str]](
            id=ID_INPUT_DESC,
            type_factory=optional_str_factory,
            on_success=_to_menu
        ),
        state=CategoryCreateSG.input_desc
    ),
)
