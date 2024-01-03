from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bot.states.dialogs import CategoryCreateSG
from app.bot.utils.optional_str import optional_str_factory
from app.bot.widgets import CANCEL_TEXT, BACK_TEXT
from app.core.domain.dto.category import CreateCategoryDTO
from app.core.interfaces.usecase.category import CategoryUsecase


async def _to_menu(_: Message, __, manager: DialogManager, ___: str):
    await manager.switch_to(CategoryCreateSG.menu_idle)


def _get_values(manager: DialogManager) -> tuple[str, Optional[str]]:
    title_input: ManagedTextInput[str] = manager.find(ID_INPUT_TITLE)
    desc_input: ManagedTextInput[Optional[str]] = manager.find(ID_INPUT_DESC)

    return title_input.get_value(), desc_input.get_value()


async def menu_getter(dialog_manager: DialogManager, **_):
    title, desc = _get_values(dialog_manager)
    return dict(title=title, desc=desc)


async def create_category(call: CallbackQuery, _: Button, manager: DialogManager):
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    title, desc = _get_values(manager)
    category = await category_service.save_category(CreateCategoryDTO(
        title=title,
        desc=desc,
        user_id=call.from_user.id
    ))

    await manager.done(dict(category_id=category.id, category=category))


ID_INPUT_TITLE = "input_title"
ID_INPUT_DESC = "input_desc"

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
