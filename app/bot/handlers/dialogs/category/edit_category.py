from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Cancel, Row, Checkbox, \
    Column, ManagedCheckbox
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bot.states.dialogs import CategoryEditSG
from app.bot.widgets import BACK_TEXT_RU, BackTo, CLOSE_TEXT_RU
from app.core.domain.dto.category import UpdateCategoryDTO
from app.core.domain.models.category import CategoryId, Category
from app.core.interfaces.usecase.category import CategoryUsecase

_ON_START_SET_DATA = "__on_startup_setup"
_FAVORITE_ID = "favorite"


async def _get_category(manager: DialogManager) -> Category:
    category = manager.dialog_data.get("category")
    if isinstance(category, Category):
        return category

    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category_id: CategoryId = manager.dialog_data["category_id"]

    category = await category_service.get_category(category_id)
    manager.dialog_data["category"] = category
    return category

async def _input_title_handler(m: Message, _: MessageInput, manager: DialogManager):
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category_id: CategoryId = manager.dialog_data["category_id"]
    manager.dialog_data["category"] = await category_service.update_category(UpdateCategoryDTO(
        category_id=category_id,
        title=m.text
    ))
    await manager.switch_to(CategoryEditSG.main)


async def _input_desc_handler(m: Message, _: MessageInput, manager: DialogManager):
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category_id: CategoryId = manager.dialog_data["category_id"]
    manager.dialog_data["category"] = await category_service.update_category(UpdateCategoryDTO(
        category_id=category_id,
        desc=m.text
    ))
    await manager.switch_to(CategoryEditSG.main)



async def _process_click_favorite(event: CallbackQuery, m: ManagedCheckbox, manager: DialogManager):
    if event.data == _ON_START_SET_DATA:
        return

    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category_id: CategoryId = manager.dialog_data["category_id"]
    manager.dialog_data["category"] = await category_service.update_category(UpdateCategoryDTO(
        category_id=category_id,
        favorite=m.is_checked()
    ))
    await manager.switch_to(CategoryEditSG.main)


async def _process_delete_desc(_: CallbackQuery, __: Button, manager: DialogManager):
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category_id: CategoryId = manager.dialog_data["category_id"]
    manager.dialog_data["category"] = await category_service.update_category(UpdateCategoryDTO(
        category_id=category_id,
        delete_desc=True,
    ))
    await manager.switch_to(CategoryEditSG.main)


async def menu_getter(dialog_manager: DialogManager, **_):
    category = await _get_category(dialog_manager)
    return dict(title=category.title, desc=category.description)


async def _desc_window_getter(dialog_manager: DialogManager, **_):
    category = await _get_category(dialog_manager)
    return dict(have_desc=category is not None)

async def _on_start(start_data: dict, manager: DialogManager):
    manager.dialog_data["category_id"] = start_data["category_id"]
    category = await _get_category(manager)
    if category.is_favorite:
        m: ManagedCheckbox = manager.find(_FAVORITE_ID)
        await m.widget.set_checked(
            manager.event.model_copy(update=dict(data=_ON_START_SET_DATA)),
            True,
            manager
        )

category_edit_dialog = Dialog(
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
                    state=CategoryEditSG.title
                ),
                SwitchTo(
                    Const("📝 Описание"),
                    id="create_category_edit_desc",
                    state=CategoryEditSG.desc
                ),
            ),
            Checkbox(
                Const("✅ Избранное"),
                Const("❌ Избранное"),
                id=_FAVORITE_ID,
                on_state_changed=_process_click_favorite

            ),
            Cancel(CLOSE_TEXT_RU)
        ),
        getter=menu_getter,
        state=CategoryEditSG.main,
    ),

    Window(
        Const("Отправьте название для категории"),
        Back(BACK_TEXT_RU),
        MessageInput(_input_title_handler),
        state=CategoryEditSG.title
    ),

    Window(
        Const("Отправьте описание для категории"),
        Column(
            Button(
                Const("Удалить описание"),
                id="delete_desc",
                on_click=_process_delete_desc,
                when="have_desc",
            ),
            BackTo(CategoryEditSG.main, BACK_TEXT_RU),
        ),
        MessageInput(_input_desc_handler),
        getter=_desc_window_getter,
        state=CategoryEditSG.desc
    ),
    on_start=_on_start
)
