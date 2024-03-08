from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import (
    Column,
    SwitchTo,
    Select,
    Cancel,
    ScrollingGroup,
    Group,
    ListGroup,
    Start
)
from aiogram_dialog.widgets.kbd.button import OnClick, Button
from aiogram_dialog.widgets.text import Format, Const
from aiogram_i18n import I18nContext
from magic_filter import F

from app.bot.services.category_finders import (
    CategoryFinder,
    TitleCategoriesFinder,
    PopularCategoriesFinder,
    FavoriteCategoriesFinder,
    MarkedCategoriesFinder,
    FindMode
)
from app.bot.states.dialogs import CategoryFindSG, CategoryCreateSG
from app.bot.widgets import BackTo, Emoji
from app.bot.widgets.i18n import BACK_TEXT, CANCEL_TEXT, TL, BackToI18n, I18N_KEY
from app.core.domain.models.category import CategoryId
from app.core.domain.models.user import User
from app.core.interfaces.usecase import CategoryUsecase

FIND_MODE_KEY = "find_mode"

MARKERS_PER_ROW = 5


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


async def _process_input_title(_, __, manager: DialogManager, ___):
    await manager.next()


async def process_click_category(_, __, manager: DialogManager, item_id: CategoryId):
    await manager.done(dict(category_id=int(item_id)))


async def _on_click_back(_, __, manager: DialogManager):
    del manager.dialog_data[FIND_MODE_KEY]


async def _on_click_empty_marker(event: CallbackQuery, _, manager: DialogManager):
    i18n: I18nContext = manager.middleware_data[I18N_KEY]
    await event.answer(
        i18n.get("about-category-marker"),
        show_alert=True,
    )


def _switch_mode_on_click(mode: FindMode) -> OnClick:
    async def _on_click(_, __, manager: DialogManager):
        manager.dialog_data[FIND_MODE_KEY] = mode

    return _on_click


async def _process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        await manager.done(dict(category_id=result["category_id"]))


async def _main_getter(user: User, category_service: CategoryUsecase, dialog_manager: DialogManager,
                       **_):
    finder = MarkedCategoriesFinder(dialog_manager, user, category_service)
    marked_categories = await finder.find_categories()

    to_min = 0
    if len(marked_categories) < MARKERS_PER_ROW:
        to_min = MARKERS_PER_ROW - len(marked_categories)

    return {
        "markers": marked_categories,
        "to_min": to_min
    }


ID_INPUT_TITLE = "find_title"

tl = TL.category.find

# Input: allowed_create - bool [Optional]
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
            Start(
                Emoji("🆕", tl.btn.create()),
                id="category_create",
                state=CategoryCreateSG.input_title,
                when=F["start_data"]["allow_create"]
            ),
        ),
        Group(
            Select(
                Format("{item.marker}"),
                id="select_category",
                on_click=process_click_category,
                type_factory=lambda c: CategoryId(int(c)),
                item_id_getter=lambda category: category.id,
                items="markers",
            ),
            ListGroup(
                Button(
                    Const(" "),
                    id="show_markers_info",
                    on_click=_on_click_empty_marker
                ),
                id="markers_padding",
                item_id_getter=lambda _: "marker_padding",
                items=lambda data: range(data["to_min"]),
                when=F["to_min"] > 0
            ),
            width=5,
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
    ),
    on_process_result=_process_result,
)
