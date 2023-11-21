from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from core.domain.category import CreateCategoryDTO


class CreateSG(StatesGroup):
    input_title = State()
    menu_idle = State()
    input_desc = State()


async def input_title_handler(m: Message, _: MessageInput, manager: DialogManager):
    manager.dialog_data["title"] = m.text
    await manager.switch_to(CreateSG.menu_idle)


async def input_desc_handler(m: Message, _: MessageInput, manager: DialogManager):
    manager.dialog_data["desc"] = m.text
    await manager.switch_to(CreateSG.menu_idle)


async def menu_getter(dialog_manager: DialogManager, **_):
    title = dialog_manager.dialog_data["title"]
    desc = dialog_manager.dialog_data.get("desc")
    return dict(title=title, desc=desc, have_desc=desc is not None)


async def create_category(call: CallbackQuery, _: Button, manager: DialogManager):
    category_service = manager.middleware_data["category_service"]
    category = await category_service.create_category(CreateCategoryDTO(
        title=manager.dialog_data["title"],
        desc=manager.dialog_data.get("desc"),
        user_id=call.from_user.id
    ))

    await manager.done(dict(category_id=category.id, category=category))


category_create_dialog = Dialog(
    Window(
        Const("Отправь название категории"),
        MessageInput(input_title_handler),
        state=CreateSG.input_title,
    ),

    Window(
        Multi(
            Format("Название: {title}"),
            Format("Описание: {desc}", when="have_desc")
        ),
        Group(
            Row(

                SwitchTo(
                    Const("Изменить название"),
                    id="create_category_edit_title",
                    state=CreateSG.input_title
                ),
                SwitchTo(
                    Const("Изменить описание"),
                    id="create_category_edit_desc",
                    state=CreateSG.input_desc
                ),
            ),
            Button(
                Const("Создать"),
                id="create_category",
                on_click=create_category,
            ),
            Cancel()
        ),
        getter=menu_getter,
        state=CreateSG.menu_idle,
    ),

    Window(
        Const("Отправьте описание для категории"),
        Back(Const("Назад")),
        MessageInput(input_desc_handler),
        state=CreateSG.input_desc
    ),

)