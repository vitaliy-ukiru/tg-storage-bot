__all__ = (
    'main_window',
)

from typing import Union

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Button, Row, Keyboard

from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Const, Format, Case, Multi, List
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from magic_filter import F

from app.bot.states.dialogs import FileListSG, CategoryFindSG
from app.bot.utils.file_type_str import get_file_type_name
from app.core.interfaces.usecase.category import CategoryUsecase
from .common import SELECT_FILE_TYPES_ID

_filters = F["dialog_data"]["filters"]


async def _main_window_getter(dialog_manager: DialogManager, category_service: CategoryUsecase, **_):
    filters = dialog_manager.dialog_data.get("filters")
    if not filters:
        return {}

    category_id = filters.get("category_id")
    if category_id is None:
        return {}

    category = await category_service.get_category(category_id)
    return {
        "category_name": category.title
    }


def file_types_names(data: dict) -> list[str]:
    return [
        get_file_type_name(ft)
        for ft in data["dialog_data"]["filters"]["file_types"]
    ]


_main_menu_text = Multi(
    Multi(
        Const("Типы файлов"),
        List(
            Format("{item}"),
            sep=', ',
            items=file_types_names
        ),
        sep=': ',
        when=_filters["file_types"],
    ),
    Format(
        text="Название: {dialog_data[filters][title]}",
        when=_filters["title"],
    ),
    Format(
        text="Категория: {category_name}",
        when="category_name"
    ),
),


def setup_button(
    *buttons: Keyboard, field_name: str,
    delete_callback: Union[OnClick, WidgetEventProcessor, None]
) -> Row:
    return Row(
        *buttons,
        Button(
            Const("❌"),
            id=f'delete_{field_name}',
            on_click=delete_callback,
            when=_filters[field_name]
        ),
    )


def _delete_from_filters(manager: DialogManager, key: str):
    filters = manager.dialog_data["filters"]
    del filters[key]


def new_delete_callback(key: str):
    async def wrapper(_, __, manager: DialogManager):
        _delete_from_filters(manager, key)

    return wrapper


async def _process_delete_file_types(_, __, manager: DialogManager):
    _delete_from_filters(manager, "file_types")
    await manager.find(SELECT_FILE_TYPES_ID).reset_checked()


main_window = Window(
    Case(
        {
            0: Const("Фильтры не установлены"),
            None: Const("Фильтры не установлены"),
            ...: _main_menu_text
        },
        selector=_filters.len() or 0
    ),
    setup_button(
        Start(
            Const("🗂 Категория"),
            state=CategoryFindSG.main,
            id="category"
        ),
        field_name="category_id",
        delete_callback=new_delete_callback("category_id")
    ),
    setup_button(
        SwitchTo(
            Const("🏷 Тип файла"),
            state=FileListSG.input_file_type,
            id="file_types"
        ),
        field_name="file_types",
        delete_callback=_process_delete_file_types,
    ),

    setup_button(
        SwitchTo(
            Const("📃 Название файла"),
            state=FileListSG.input_file_title,
            id="file_title"
        ),
        delete_callback=new_delete_callback("title"),
        field_name="title"
    ),

    SwitchTo(
        Const("🔎 Поиск"),
        state=FileListSG.file_list,
        id="find_files",
    ),
    state=FileListSG.main,
    getter=_main_window_getter,
)
