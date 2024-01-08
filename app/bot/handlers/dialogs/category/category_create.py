from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bot.states.dialogs import CategoryCreateSG
from app.bot.utils.optional_str import optional_str_factory
from app.bot.widgets import CANCEL_TEXT, BACK_TEXT
from app.bot.widgets.dao.base_dao import BaseDAO
from app.bot.widgets.dao.widgets import TextInputProp
from app.core.domain.dto.category import CreateCategoryDTO
from app.core.interfaces.usecase.category import CategoryUsecase

ID_INPUT_TITLE = "input_title"
ID_INPUT_DESC = "input_desc"


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
        Const("Отправь название категории"),
        TextInput(id=ID_INPUT_TITLE, on_success=_to_menu),
        state=CategoryCreateSG.input_title,
    ),

    Window(
        Multi(
            Format("Название: {title}"),
            Format("Описание: {desc}", when="desc")
        ),
        Group(
            Row(
                SwitchTo(
                    Const("📝 Название"),
                    id="edit_title",
                    state=CategoryCreateSG.input_title
                ),
                SwitchTo(
                    Const("📝 Описание"),
                    id="edit_desc",
                    state=CategoryCreateSG.input_desc
                ),
            ),
            Button(
                Const("✅ Создать"),
                id="create",
                on_click=create_category,
            ),
            Cancel(CANCEL_TEXT)
        ),
        getter=menu_getter,
        state=CategoryCreateSG.menu_idle,
    ),

    Window(
        Const("Отправьте описание для категории"),
        Back(BACK_TEXT),
        TextInput[Optional[str]](
            id=ID_INPUT_DESC,
            type_factory=optional_str_factory,
            on_success=_to_menu
        ),
        state=CategoryCreateSG.input_desc
    ),
)
