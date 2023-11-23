from typing import Any

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Select, Group, Cancel
from aiogram_dialog.widgets.text import Const, Format

from bot.handlers.dialogs.back import BackTo
from bot.middlewares.user_manager import USER_KEY
from core.domain.models.user import User
from core.domain.services.category import CategoryUsecase


class FindSG(StatesGroup):
    select_topic = State()
    top = State()
    input_title = State()
    find = State()


async def process_click_category(_: CallbackQuery, _1: Any, manager: DialogManager, item_id: str):
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

    categories = await category_service.find_top_5_popular(user.id)
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

find_category_dialog = Dialog(
    Window(
        Const("Выберите раздел"),
        Column(
            SwitchTo(
                Const("Самые используемые"),
                id="category_exists_top",
                state=FindSG.top,
            ),
            SwitchTo(
                Const("Поиск по названию"),
                id="category_exists_find",
                state=FindSG.find,
            ),
            Cancel(),
        ),
        state=FindSG.select_topic,
    ),
    Window(
        Const("Выберите категорию"),
        Group(
            _select_category,
            width=2,
        ),
        BackTo(FindSG.select_topic),
        getter=_category_top_getter,
        state=FindSG.top
    ),

    Window(
        Const("Введите часть названия категории"),
        MessageInput(_process_input_title),
        BackTo(FindSG.select_topic),
        state=FindSG.input_title,
    ),
    Window(
        Group(
            _select_category,
            width=2
        ),
        BackTo(FindSG.select_topic),
        state=FindSG.find,
        getter=_category_find_getter,
    ),

)
