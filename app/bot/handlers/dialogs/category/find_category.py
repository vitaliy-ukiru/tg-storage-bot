from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Select, Cancel, ScrollingGroup, Row
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Format

from app.bot.states.dialogs import CategoryFindSG
from app.bot.services.category_finders import (
    CategoryFinder,
    TitleCategoriesFinder,
    PopularCategoriesFinder,
    FavoriteCategoriesFinder,
    MarkedCategoriesFinder,
    FindMode
)
from app.bot.widgets import BackTo
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import BACK_TEXT, CANCEL_TEXT, TL, BackToI18n
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
            title: ManagedTextInput = dialog_manager.find(ID_INPUT_TITLE)
            finder = TitleCategoriesFinder(dialog_manager, user, category_service, title.get_value())
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


async def _on_click_back(_, __, manager: DialogManager):
    del manager.dialog_data[FIND_MODE_KEY]


def _switch_mode_on_click(mode: FindMode) -> OnClick:
    async def _on_click(_, __, manager: DialogManager):
        manager.dialog_data[FIND_MODE_KEY] = mode

    return _on_click


async def _main_getter(user: User, category_service: CategoryUsecase, dialog_manager: DialogManager,
                       **_):
    finder = MarkedCategoriesFinder(dialog_manager, user, category_service)
    marked_categories = await finder.find_categories()
    return {
        "markers": marked_categories
    }


ID_INPUT_TITLE = "find_title"

tl = TL.category.find

find_category_dialog = Dialog(
    Window(
        tl.select.method(),
        Column(
            SwitchTo(
                Emoji("🔝", tl.btn.popular()),
                id="category_exists_top",
                on_click=_switch_mode_on_click(FindMode.popular),
                state=CategoryFindSG.select,
            ),
            SwitchTo(
                Emoji("⭐", tl.btn.favorites()),
                id="category_exists_favorites",
                on_click=_switch_mode_on_click(FindMode.favorite),
                state=CategoryFindSG.select
            ),
            SwitchTo(
                Emoji("🔎", tl.btn.title()),
                id="category_exists_find",
                on_click=_switch_mode_on_click(FindMode.title),
                state=CategoryFindSG.input_title,
            ),
        ),
        Row(
            Select(
                Format("{item.marker}"),
                id="select_category",
                on_click=process_click_category,
                type_factory=lambda c: CategoryId(int(c)),
                item_id_getter=lambda category: category.id,
                items="markers",
            ),
        ),
        Cancel(CANCEL_TEXT),
        getter=_main_getter,
        state=CategoryFindSG.main,
    ),
    Window(
        tl.input.title(),
        TextInput(id=ID_INPUT_TITLE, on_success=_process_input_title),
        BackTo(CategoryFindSG.main, BACK_TEXT),
        state=CategoryFindSG.input_title,
    ),
    Window(
        tl.result(),
        ScrollingGroup(
            Select[CategoryId](
                Format("{item.title}"),
                id="select_category",
                on_click=process_click_category,
                type_factory=lambda c: CategoryId(int(c)),
                item_id_getter=lambda category: category.id,
                items="categories",
            ),
            id="select_category_scroll",
            width=2,
            height=2,
            hide_on_single_page=True,
        ),
        BackToI18n(
            CategoryFindSG.main,
            on_click=_on_click_back
        ),
        state=CategoryFindSG.select,
        getter=_category_generic_getter,
    )
)
