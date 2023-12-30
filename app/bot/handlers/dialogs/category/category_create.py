from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bot.widgets import CANCEL_TEXT, BACK_TEXT
from app.bot.states.dialogs import CategoryCreateSG
from app.core.domain.dto.category import CreateCategoryDTO
from app.core.interfaces.usecase.category import CategoryUsecase


async def input_title_handler(m: Message, _: MessageInput, manager: DialogManager):
    manager.dialog_data["title"] = m.text
    await manager.switch_to(CategoryCreateSG.menu_idle)


async def input_desc_handler(m: Message, _: MessageInput, manager: DialogManager):
    manager.dialog_data["desc"] = m.text
    await manager.switch_to(CategoryCreateSG.menu_idle)


async def menu_getter(dialog_manager: DialogManager, **_):
    title = dialog_manager.dialog_data["title"]
    desc = dialog_manager.dialog_data.get("desc")
    return dict(title=title, desc=desc)


async def create_category(call: CallbackQuery, _: Button, manager: DialogManager):
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category = await category_service.save_category(CreateCategoryDTO(
        title=manager.dialog_data["title"],
        desc=manager.dialog_data.get("desc"),
        user_id=call.from_user.id
    ))

    await manager.done(dict(category_id=category.id, category=category))


category_create_dialog = Dialog(
    Window(
        Const("Отправь название категории"),
        MessageInput(input_title_handler),
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
                    id="create_category_edit_title",
                    state=CategoryCreateSG.input_title
                ),
                SwitchTo(
                    Const("📝 Описание"),
                    id="create_category_edit_desc",
                    state=CategoryCreateSG.input_desc
                ),
            ),
            Button(
                Const("✅ Создать"),
                id="create_category",
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
        MessageInput(input_desc_handler),
        state=CategoryCreateSG.input_desc
    ),

)
