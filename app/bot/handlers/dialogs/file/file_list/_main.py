__all__ = (
    'main_window',
)

from typing import Union, Callable, Awaitable

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Button, Row, Keyboard
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Const, Format, Case, Multi, List
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from magic_filter import F

from app.bot.states.dialogs import FileListSG, CategoryFindSG
from app.bot.utils.file_type_str import get_file_type_name
from app.core.interfaces.usecase.category import CategoryUsecase
from .filters_dao import FiltersDAO

_filters = F["filters"]


async def _main_window_getter(dialog_manager: DialogManager, category_service: CategoryUsecase, **_):
    filters_dao = FiltersDAO(dialog_manager)
    filters = filters_dao.extract_to_dict()
    data = {
        "filters": filters
    }

    if (category_id := filters.get("category_id")) is not None:
        category = await category_service.get_category(category_id)
        data["category_name"] = category.title

    return data


_main_menu_text = Multi(
    Multi(
        Const("Типы файлов"),
        List(
            Format("{item}"),
            sep=', ',
            items=lambda data: [
                get_file_type_name(ft)
                for ft in data["filters"]["file_types"]
            ]
        ),
        sep=': ',
        when=_filters["file_types"],
    ),
    Format(
        text="Название: {filters[title]}",
        when=_filters["title"],
    ),
    Format(
        text="Категория: {category_name}",
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
async def _delete_category(fitlers: FiltersDAO):
    del fitlers.category


main_window = Window(
    Case(
        {
            0: Const("Фильтры не установлены"),
            ...: _main_menu_text
        },
        selector=_filters.len() or 0
    ),
    new_filter_btn(
        Start(
            Const("🗂 Категория"),
            state=CategoryFindSG.main,
            id="category"
        ),
        field_name="category_id",
        delete_callback=_delete_category
    ),
    new_filter_btn(
        SwitchTo(
            Const("🏷 Тип файла"),
            state=FileListSG.input_file_type,
            id="file_types"
        ),
        field_name="file_types",
        delete_callback=_delete_file_types
    ),
    new_filter_btn(
        SwitchTo(
            Const("📃 Название файла"),
            state=FileListSG.input_file_title,
            id="file_title"
        ),
        field_name="title",
        delete_callback=_delete_title
    ),

    SwitchTo(
        Const("🔎 Поиск"),
        state=FileListSG.file_list,
        id="find_files",
    ),
    state=FileListSG.main,
    getter=_main_window_getter,
)
