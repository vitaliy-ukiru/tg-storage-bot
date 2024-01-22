from typing import cast

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Select, Cancel, ScrollingGroup
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Const, Format

from app.bot.states.dialogs import CategoryFindSG
from app.bot.utils.category_finders import (CategoryFinder, TitleCategoriesFinder,
                                            PopularCategoriesFinder,
                                            FavoriteCategoriesFinder, FindMode)
from app.bot.widgets import BackTo
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import BACK_TEXT, CANCEL_TEXT, LC, Template, BackToI18n
from app.core.domain.models.category import CategoryId
from app.core.domain.models.user import User
from app.core.interfaces.usecase.category import CategoryUsecase

FIND_MODE_KEY = "find_mode"


async def _process_input_title(_, __, manager: DialogManager, ___):
    await manager.next()


async def _category_generic_getter(dialog_manager: DialogManager,
                                   category_service: CategoryUsecase,
                                   user: User, **_):
    mode: FindMode = dialog_manager.dialog_data[FIND_MODE_KEY]
    finder: CategoryFinder
    match mode:
        case FindMode.title:
            title = cast(ManagedTextInput, dialog_manager.find(ID_INPUT_TITLE)).get_value()
            finder = TitleCategoriesFinder(dialog_manager, user, category_service, title)
        case FindMode.favorite:
            finder = FavoriteCategoriesFinder(dialog_manager, user, category_service)
        case _:
            # popular finder will default
            finder = PopularCategoriesFinder(dialog_manager, user, category_service)

    categories = await finder.find_categories()
    return {
        "categories": categories,
        "mode": mode
    }


async def process_click_category(_, __, manager: DialogManager, item_id: CategoryId):
    await manager.done(dict(category_id=int(item_id)))


_select_category = Select[CategoryId](
    Format("{item.title}"),
    id="select_category",
    on_click=process_click_category,
    type_factory=lambda c: CategoryId(int(c)),
    item_id_getter=lambda category: category.id,
    items="categories",
)

_scroll_categories = ScrollingGroup(
    _select_category,
    id="select_category_scroll",
    width=2,
    height=2,
    hide_on_single_page=True,
)


async def _on_click_back(_, __, manager: DialogManager):
    del manager.dialog_data[FIND_MODE_KEY]


def _switch_mode_on_click(mode: FindMode) -> OnClick:
    async def _on_click(_, __, manager: DialogManager):
        manager.dialog_data[FIND_MODE_KEY] = mode

    return _on_click


ID_INPUT_TITLE = "find_title"


lc = LC.category.find

find_category_dialog = Dialog(
    Window(
        Template(lc.select.method),
        Column(
            SwitchTo(
                Emoji("🔝", Template(lc.btn.popular)),
                id="category_exists_top",
                on_click=_switch_mode_on_click(FindMode.popular),
                state=CategoryFindSG.select,
            ),
            SwitchTo(
                Emoji("⭐", Template(lc.btn.favorites)),
                id="category_exists_favorites",
                on_click=_switch_mode_on_click(FindMode.favorite),
                state=CategoryFindSG.select
            ),
            SwitchTo(
                Emoji("🔎", Template(lc.btn.title)),
                id="category_exists_find",
                on_click=_switch_mode_on_click(FindMode.title),
                state=CategoryFindSG.input_title,
            ),
            Cancel(CANCEL_TEXT),
        ),
        state=CategoryFindSG.main,
    ),
    Window(
        Template(lc.input.title),
        TextInput(id=ID_INPUT_TITLE, on_success=_process_input_title),
        BackTo(CategoryFindSG.main, BACK_TEXT),
        state=CategoryFindSG.input_title,
    ),
    Window(
        Template(lc.result),
        _scroll_categories,
        BackToI18n(
            CategoryFindSG.main,
            on_click=_on_click_back
        ),
        state=CategoryFindSG.select,
        getter=_category_generic_getter,
    )
)
