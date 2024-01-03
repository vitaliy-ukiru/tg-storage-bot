from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput, TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Cancel, Row, Checkbox, \
    Column, ManagedCheckbox
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.bot.states.dialogs import CategoryEditSG
from app.bot.widgets import BACK_TEXT, BackTo, CLOSE_TEXT
from app.core.domain.dto.category import UpdateCategoryDTO
from app.core.domain.models.category import CategoryId, Category
from app.core.interfaces.usecase.category import CategoryUsecase

_ON_START_SET_DATA = "__on_startup_setup"
_FAVORITE_ID = "favorite"


async def _update_category(
    manager: DialogManager,
    title: Optional[str] = None,
    desc: Optional[str] = None,
    delete_desc: Optional[bool] = None,
    favorite: Optional[bool] = None,
) -> Category:
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category_id: CategoryId = manager.dialog_data["category_id"]
    category = await category_service.update_category(UpdateCategoryDTO(
        category_id=category_id,
        title=title,
        desc=desc,
        delete_desc=delete_desc,
        favorite=favorite
    ))
    manager.dialog_data["category"] = category
    return category


async def _get_category(manager: DialogManager) -> Category:
    category = manager.dialog_data.get("category")
    if isinstance(category, Category):
        return category

    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    category_id: CategoryId = manager.dialog_data["category_id"]

    category = await category_service.get_category(category_id)
    manager.dialog_data["category"] = category
    return category


async def _input_title_handler(_, __, manager: DialogManager, text: str):
    await _update_category(manager, title=text)
    await manager.switch_to(CategoryEditSG.main)


async def _input_desc_handler(_, __, manager: DialogManager, text: str):
    await _update_category(manager, desc=text)
    await manager.switch_to(CategoryEditSG.main)


async def _process_click_favorite(event: CallbackQuery, m: ManagedCheckbox, manager: DialogManager):
    if event.data == _ON_START_SET_DATA:
        return

    await _update_category(manager, favorite=m.is_checked())
    await manager.switch_to(CategoryEditSG.main)


async def _process_delete_desc(_, __, manager: DialogManager):
    await _update_category(manager, delete_desc=True)
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
            # for identification and not update in service
            # see _process_click_favorite
            manager.event.model_copy(
                update=dict(data=_ON_START_SET_DATA)
            ),
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
            Cancel(CLOSE_TEXT)
        ),
        getter=menu_getter,
        state=CategoryEditSG.main,
    ),

    Window(
        Const("Отправьте название для категории"),
        Back(BACK_TEXT),
        TextInput(id="edit__input_title", on_success=_input_title_handler),
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
            BackTo(CategoryEditSG.main, BACK_TEXT),
        ),
        TextInput(id="edit__input_desc", on_success=_input_desc_handler),
        getter=_desc_window_getter,
        state=CategoryEditSG.desc
    ),
    on_start=_on_start
)


class CategoryDescription:
    description: Optional[str]
