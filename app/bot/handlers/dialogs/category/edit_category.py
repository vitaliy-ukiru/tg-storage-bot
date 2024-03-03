from functools import wraps
from typing import Optional, Any, Callable, TypeAlias, Awaitable

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.common import ManagedWidget
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Cancel, Row, Checkbox, \
    Column, ManagedCheckbox
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_i18n import I18nContext

from app.bot.states.dialogs import CategoryEditSG
from app.bot.widgets.dao import DialogDataProp, DialogDataRequiredProp
from app.bot.widgets.dao.base_dao import BaseDAO
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import BACK_TEXT, CLOSE_TEXT, TL, Topic, BackToI18n
from app.core.domain.dto.category import UpdateCategoryDTO
from app.core.domain.exceptions.category import InvalidCategoryMarker
from app.core.domain.models.category import CategoryId, Category
from app.core.interfaces.usecase.category import CategoryUsecase

_ON_START_SET_DATA = "__on_startup_setup$$$$$"
_FAVORITE_ID = "favorite"


class UpdateDAO(BaseDAO):
    category_id: CategoryId = DialogDataRequiredProp[CategoryId]("category_id")
    __category_cache = DialogDataProp[Category | Any]("category")

    async def get_category(self) -> Category:
        category = self.__category_cache
        if isinstance(category, Category):
            return category

        svc = self.category_service

        category = await svc.get_category(self.category_id)
        self.__category_cache = category
        return category

    @property
    def category_service(self) -> CategoryUsecase:
        return self.manager.middleware_data["category_service"]

    def __category_setter(self, value: Category):
        self.__category_cache = value

    category = property(fset=__category_setter)


async def _update_category(
    manager: DialogManager,
    title: Optional[str] = None,
    desc: Optional[str] = None,
    delete_desc: Optional[bool] = None,
    favorite: Optional[bool] = None,
    marker: Optional[str] = None,
    delete_marker: Optional[bool] = None
) -> Category:
    data = UpdateDAO(manager)
    category_service = data.category_service
    category_id = data.category_id
    category = await category_service.update_category(UpdateCategoryDTO(
        category_id=category_id,
        title=title,
        desc=desc,
        delete_desc=delete_desc,
        favorite=favorite,
        marker=marker,
        delete_marker=delete_marker,
    ))
    data.category = category
    return category


async def _get_category(manager: DialogManager) -> Category:
    dao = UpdateDAO(manager)
    return await dao.get_category()


CallbackType: TypeAlias = Callable[[ChatEvent, ManagedWidget, DialogManager, ...], Awaitable]


def switcher(state: State):
    def wrap_func(fn: CallbackType):
        @wraps(fn)
        async def wrapper(event, widget, manager: DialogManager, *args, **kwargs):
            await fn(event, widget, manager, *args, **kwargs)
            await manager.switch_to(state)

        return wrapper

    return wrap_func


@switcher(CategoryEditSG.main)
async def _input_title_handler(_, __, manager: DialogManager, text: str):
    await _update_category(manager, title=text)


@switcher(CategoryEditSG.main)
async def _input_desc_handler(_, __, manager: DialogManager, text: str):
    await _update_category(manager, desc=text)


async def _input_marker_handler(m: Message, __, manager: DialogManager, text: str):
    try:
        await _update_category(manager, marker=text)
    except InvalidCategoryMarker:
        i18n: I18nContext = manager.middleware_data["i18n"]
        await m.answer(i18n.get("category-invalid-marker"))
    else:
        await manager.switch_to(CategoryEditSG.main)


async def _process_click_favorite(event: CallbackQuery, m: ManagedCheckbox, manager: DialogManager):
    if event.data == _ON_START_SET_DATA:
        return

    await _update_category(manager, favorite=m.is_checked())
    await manager.switch_to(CategoryEditSG.main)


@switcher(CategoryEditSG.main)
async def _process_delete_desc(_, __, manager: DialogManager):
    await _update_category(manager, delete_desc=True)


@switcher(CategoryEditSG.main)
async def _process_delete_marker(_, __, manager: DialogManager):
    await _update_category(manager, delete_marker=True)


async def menu_getter(dialog_manager: DialogManager, **_):
    category = await _get_category(dialog_manager)
    return dict(title=category.title, desc=category.description, marker=category.marker)


async def _desc_window_getter(dialog_manager: DialogManager, **_):
    category = await _get_category(dialog_manager)
    return dict(have_desc=category.description is not None)


async def _marker_window_getter(dialog_manager: DialogManager, **_):
    category = await _get_category(dialog_manager)
    return dict(have_marker=category.marker is not None)


async def _on_start(start_data: dict, manager: DialogManager):
    dao = UpdateDAO(manager)
    dao.category_id = start_data["category_id"]
    category = await dao.get_category()

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


tl = TL.category.edit

favorite_template = tl.btn.favorite()

category_edit_dialog = Dialog(
    Window(
        Multi(
            Topic(TL.category.marker(), Format("{marker}"), when="marker"),
            Topic(TL.category.title(), Format("{title}")),
            Topic(TL.category.desc(), Format("{desc}"), when="desc")
        ),
        Group(
            Row(
                SwitchTo(
                    Emoji("📝", tl.btn.title()),
                    id="create_category_edit_title",
                    state=CategoryEditSG.title
                ),
                SwitchTo(
                    Emoji("📝", tl.btn.desc()),
                    id="create_category_edit_desc",
                    state=CategoryEditSG.desc
                ),
            ),
            Checkbox(
                Emoji("✅", favorite_template),
                Emoji("❌", favorite_template),
                id=_FAVORITE_ID,
                on_state_changed=_process_click_favorite

            ),
            SwitchTo(
                Emoji("🟢", tl.btn.marker()),
                id="edit_marker",
                state=CategoryEditSG.marker,
            ),
            Cancel(CLOSE_TEXT)
        ),
        getter=menu_getter,
        state=CategoryEditSG.main,
    ),

    Window(
        tl.input.title(),
        Back(BACK_TEXT),
        TextInput(id="edit__input_title", on_success=_input_title_handler),
        state=CategoryEditSG.title
    ),

    Window(
        tl.input.desc(),
        Column(
            Button(
                tl.btn.delete.desc(),
                id="delete_desc",
                on_click=_process_delete_desc,
                when="have_desc",
            ),
            BackToI18n(CategoryEditSG.main),
        ),
        TextInput(id="edit__input_desc", on_success=_input_desc_handler),
        getter=_desc_window_getter,
        state=CategoryEditSG.desc
    ),
    Window(
        tl.input.marker(),
        Column(
            Button(
                tl.btn.delete.marker(),
                id="delete_marker",
                on_click=_process_delete_marker,
                when="have_marker",
            ),
            BackToI18n(CategoryEditSG.main),
        ),
        TextInput(id="edit__input_marker", on_success=_input_marker_handler),
        getter=_marker_window_getter,
        state=CategoryEditSG.marker
    ),
    on_start=_on_start
)
