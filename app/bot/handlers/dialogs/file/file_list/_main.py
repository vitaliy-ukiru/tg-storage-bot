__all__ = (
    'main_window',
)

from typing import Union, Callable, Awaitable

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Button, Row
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Const, Format, Case, Multi, List
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from aiogram_i18n import I18nContext
from magic_filter import F

from app.bot.middlewares import USER_KEY
from app.bot.states.dialogs import FileListSG, CategoryFindSG
from app.bot.utils import get_file_category_name
from app.bot.widgets import Emoji
from app.bot.widgets.i18n import Topic, CloseI18n
from app.core.domain.models.user import User
from app.core.interfaces.usecase import CategoryUsecase
from .common import tl_file_list
from .filters_dao import FiltersDAO

_filters = F["filters"]
tl = tl_file_list.main


async def _main_window_getter(dialog_manager: DialogManager, category_service: CategoryUsecase, **_):
    filters_dao = FiltersDAO(dialog_manager)
    filters = filters_dao.extract_to_dict()
    data = {
        "filters": filters,
        "have_filters": len(filters) > 0
    }
    user: User = dialog_manager.middleware_data[USER_KEY]

    if (category_id := filters.get("category_id")) is not None:
        category = await category_service.get_category(category_id, user.id)
        data["category_name"] = category.title

    return data


_main_menu_text = Multi(
    Multi(
        tl.topic.file.types(),
        List(
            Format("{item}"),
            sep=', ',
            items=lambda data: [
                get_file_category_name(ft, I18nContext.get_current())
                for ft in data["filters"]["file_types"]
            ]
        ),
        sep=': ',
        when=_filters["file_types"],
    ),
    Topic(
        tl.topic.title, Format("{filters[title]}"),
        when=_filters["title"],
    ),
    Topic(
        tl.topic.category, Format("{category_name}"),
        when="category_name"
    ),
)


def new_filter_btn(
    button: Button, field_name: str,
    delete_callback: Union[OnClick, WidgetEventProcessor, None]
) -> Row:
    return Row(
        button,
        Button(
            Const("❌"),
            id=f'delete_{field_name}',
            on_click=delete_callback,
            when=_filters[field_name]
        ),
    )


def filters_proxy_wrap(fn: Callable[[FiltersDAO], Awaitable]) -> OnClick:
    async def wrapper(_, __, manager: DialogManager):
        dao = FiltersDAO(manager)
        return await fn(dao)

    return wrapper


@filters_proxy_wrap
async def _delete_file_types(filters: FiltersDAO):
    await filters.file_types.delete()


@filters_proxy_wrap
async def _delete_title(filters: FiltersDAO):
    del filters.title


@filters_proxy_wrap
async def _delete_category(filters: FiltersDAO):
    del filters.category


main_window = Window(
    Case(
        {
            False: tl.topic.empty(),
            True: _main_menu_text
        },
        selector="have_filters"
    ),
    new_filter_btn(
        Start(
            Emoji("🗂", tl.btn.category()),
            state=CategoryFindSG.main,
            id="category"
        ),
        field_name="category_id",
        delete_callback=_delete_category
    ),
    new_filter_btn(
        SwitchTo(
            Emoji("🏷", tl.btn.file.type()),
            state=FileListSG.input_file_type,
            id="file_types"
        ),
        field_name="file_types",
        delete_callback=_delete_file_types
    ),
    new_filter_btn(
        SwitchTo(
            Emoji("📃", tl.btn.title()),
            state=FileListSG.input_file_title,
            id="file_title"
        ),
        field_name="title",
        delete_callback=_delete_title
    ),

    SwitchTo(
        Emoji("🔎", tl.btn.search()),
        state=FileListSG.file_list,
        id="find_files",
    ),
    CloseI18n(),
    state=FileListSG.main,
    getter=_main_window_getter,
)
