from typing import Any, NamedTuple

from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Start, Select, Back, Button, Row, Group
from aiogram_dialog.widgets.text import Const, Format, Multi, Case
from magic_filter import F
from sqlalchemy import Column

from bot.handlers.dialogs.custom.back import BackTo
from bot.states.dialogs import CategoryFindSG, FilterSG
from core.domain.models.file import FileType
from core.domain.services.category import CategoryUsecase


class FileTypeItem(NamedTuple):
    name: str
    value: FileType


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


def str_to_file_type(item_id: str) -> FileType:
    return FileType(item_id)


async def process_click_file_type(_: CallbackQuery, __: Any, manager: DialogManager, item_id: FileType):
    filters = manager.dialog_data.setdefault("filters", {})
    filters["file_type"] = item_id
    await manager.back()


async def _process_input_title(m: Message, _: MessageInput, dialog_manager: DialogManager):
    title_pattern = m.text
    filters = dialog_manager.dialog_data.setdefault("filters", {})
    filters["title"] = title_pattern
    await dialog_manager.switch_to(FilterSG.main)


async def _on_start(start_data: dict | Any, manager: DialogManager):
    if not isinstance(start_data, dict):
        return

    manager.dialog_data["filters"] = start_data.get("filters") or {}


async def _on_process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        filters = manager.dialog_data.setdefault("filters", {})
        filters["category_id"] = result["category_id"]


async def _on_click_done(_: CallbackQuery, __: Any, manager: DialogManager):
    filters = manager.dialog_data.get("filters", {}).copy()
    await manager.done(dict(filters=filters))


_filters = F["dialog_data"]["filters"]

filters_text = Case(
    {
        0: Const("Фильтры не установлены"),
        None: Const("Фильтры не установлены"),
        ...: Multi(
            Format(
                text="Тип файла: {dialog_data[filters][file_type].name}",
                when=_filters["file_type"],
            ),
            Format(
                text="Название: {dialog_data[filters][title]",
                when=_filters["title"],
            ),
            Format(
                text="Категория: {category_name}",
                when="category_name"
            ),
        ),
    },
    selector=_filters.len() or 0
)
filter_select_dialog = Dialog(
    Window(
        filters_text,
        Start(Const("Категория"), state=CategoryFindSG.main, id="category"),
        SwitchTo(Const("Тип файла"), state=FilterSG.file_type, id="file_type"),
        SwitchTo(Const("Название файла"), state=FilterSG.file_title, id="file_title"),
        Button(
            Const("Завершить выбор"),
            id="done",
            on_click=_on_click_done,
        ),
        getter=_main_window_getter,
        state=FilterSG.main
    ),
    Window(
        Const("Выберите тип файла"),
        Group(
            Select(
                Format("{item.name}"),
                id="select_file_type",
                type_factory=str_to_file_type,
                on_click=process_click_file_type,
                item_id_getter=lambda file_type: file_type.value,
                items="file_types",
            ),
            width=1,
        ),
        Back(),
        state=FilterSG.file_type,
        getter={
            "file_types": [
                FileTypeItem(name="Текст", value=FileType.text),
                FileTypeItem(name="Фото", value=FileType.photo),
                FileTypeItem(name="Видео", value=FileType.video),
                FileTypeItem(name="Документ", value=FileType.document),
                FileTypeItem(name="Аудио", value=FileType.audio),
                FileTypeItem(name="Гиф", value=FileType.gif),
            ]
        },
    ),
    Window(
        Const("Введите часть названия файлов"),
        MessageInput(
            _process_input_title,
            content_types=ContentType.TEXT,
        ),
        BackTo(FilterSG.main),
        state=FilterSG.file_title,
    ),
    on_process_result=_on_process_result,
    on_start=_on_start
)
