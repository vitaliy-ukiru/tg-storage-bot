from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Select, Group, Cancel, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from app.bot.widgets import BackTo, CANCEL_TEXT_RU, BACK_TEXT_RU
from app.bot.middlewares.user_manager import USER_KEY
from app.bot.states.dialogs import CategoryFindSG
from app.core.domain.models.user import User
from app.core.interfaces.usecase.category import CategoryUsecase


async def process_click_category(_: CallbackQuery, __: Any, manager: DialogManager, item_id: str):
    await manager.done(dict(category_id=int(item_id)))


async def _process_input_title(m: Message, _: MessageInput, manager: DialogManager):
    manager.dialog_data["title_mask"] = m.text
    await manager.next()


async def _category_find_getter(dialog_manager: DialogManager, category_service: CategoryUsecase, **_):
    user: User = dialog_manager.middleware_data[USER_KEY]
    title = dialog_manager.dialog_data["title_mask"]
    categories = await category_service.find_by_title(user.id, title)
    return {
        "categories": categories,
    }


async def _category_top_getter(dialog_manager: DialogManager, category_service: CategoryUsecase, **_):
    user: User = dialog_manager.middleware_data[USER_KEY]
    categories = await category_service.find_popular(user.id)
    return {
        "categories": categories,
    }


async def _category_fav_getter(dialog_manager: DialogManager, category_service: CategoryUsecase, **_):
    user: User = dialog_manager.middleware_data[USER_KEY]
    categories = await category_service.find_favorites(user.id)
    return {
        "categories": categories,
    }


_select_category = Select(
    Format("{item.title}"),
    id="select_category",
    on_click=process_click_category,
    item_id_getter=lambda category: category.id,
    items="categories",
)

_scroll_categories = ScrollingGroup(
    _select_category,
    id="select_category_scroll",
    width=2,
    height=2
)

find_category_dialog = Dialog(
    Window(
        Const("Выберите раздел"),
        Column(
            SwitchTo(
                Const("🔝 Самые используемые"),
                id="category_exists_top",
                state=CategoryFindSG.top,
            ),
            SwitchTo(
                Const("⭐ Избранные"),
                id="category_exists_favorites",
                state=CategoryFindSG.favorites
            ),
            SwitchTo(
                Const("🔎 Поиск по названию"),
                id="category_exists_find",
                state=CategoryFindSG.input_title,
            ),
            Cancel(CANCEL_TEXT_RU),
        ),
        state=CategoryFindSG.main,
    ),
    Window(
        Const("Выберите категорию"),
        _scroll_categories,
        BackTo(CategoryFindSG.main, BACK_TEXT_RU),
        getter=_category_top_getter,
        state=CategoryFindSG.top
    ),

    Window(
        Const("Выберите категорию"),
        _scroll_categories,
        BackTo(CategoryFindSG.main, BACK_TEXT_RU),
        getter=_category_fav_getter,
        state=CategoryFindSG.favorites
    ),

    Window(
        Const("Введите часть названия категории"),
        MessageInput(_process_input_title),
        BackTo(CategoryFindSG.main, BACK_TEXT_RU),
        state=CategoryFindSG.input_title,
    ),
    Window(
        Const("Список найденных категорий"),
        Group(
            _select_category,
            width=2
        ),
        BackTo(CategoryFindSG.main, BACK_TEXT_RU),
        state=CategoryFindSG.find,
        getter=_category_find_getter,
    )

)
