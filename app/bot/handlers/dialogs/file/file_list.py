from typing import Any, NamedTuple

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Select, Back, ScrollingGroup, SwitchTo, Group, Multiselect, \
    ManagedMultiselect, Button, Row
from aiogram_dialog.widgets.text import Const, Format, Case, Multi, List
from magic_filter import F

from app.bot.handlers.dialogs import execute
from app.bot.widgets import BackTo, BACK_TEXT_RU
from app.bot.middlewares.user_manager import USER_KEY
from app.bot.states.dialogs import FileListSG, CategoryFindSG
from app.bot.utils.file_type_str import file_types_with_names, get_file_type_name
from app.core.domain.dto.file import FilesFindDTO
from app.core.domain.models.file import FileType
from app.core.domain.models.user import User
from app.core.interfaces.usecase.category import CategoryUsecase
from app.core.interfaces.usecase.file import FileUsecase


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


async def _process_click_file(_: CallbackQuery, __: Select, manager: DialogManager, item_id: int):
    await execute.file_view(manager, item_id, data=dict(opened_over=True))


def _to_dto(user_id: int, filters: dict[str, Any]) -> FilesFindDTO:
    return FilesFindDTO(
        user_id=user_id,
        category_id=filters.get('category_id'),
        file_types=filters.get('file_types'),
        title_match=filters.get('title'),
    )


async def _on_process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        filters = manager.dialog_data.setdefault("filters", {})
        filters["category_id"] = result["category_id"]


SELECT_FILE_TYPES_ID = "SELECT_FILE_TYPES"


async def _on_start(start_data: dict | Any, manager: DialogManager):
    if not isinstance(start_data, dict):
        return

    filters: dict = start_data.get("filters")
    if filters is None:
        return

    file_types = filters.get('file_types')
    if file_types is not None:
        select: ManagedMultiselect[FileType] = manager.find(SELECT_FILE_TYPES_ID)
        for file_type in file_types:
            if isinstance(file_type, FileTypeItem):
                file_type = file_type.value
            await select.set_checked(file_type, False)

    manager.dialog_data["filters"] = filters


class FileTypeItem(NamedTuple):
    name: str
    value: FileType


def str_to_file_type(item_id: str) -> FileType:
    return FileType(item_id)


async def _process_state_file_type(_: CallbackQuery, select: ManagedMultiselect, manager: DialogManager,
                                   __: FileType):
    filters = manager.dialog_data.setdefault("filters", {})
    filters["file_types"] = select.get_checked()


async def _process_input_title(m: Message, _: MessageInput, dialog_manager: DialogManager):
    title_pattern = m.text
    filters = dialog_manager.dialog_data.setdefault("filters", {})
    filters["title"] = title_pattern
    await dialog_manager.switch_to(FileListSG.main)


async def _files_find_getter(dialog_manager: DialogManager, file_service: FileUsecase, **_):
    user: User = dialog_manager.middleware_data[USER_KEY]
    filters = _to_dto(user.id, dialog_manager.dialog_data.get("filters", {}))
    files = await file_service.find_files(dto=filters)
    return {
        "files": files,
    }


async def _process_delete_category(_: CallbackQuery, __: Button, manager: DialogManager):
    filters = manager.dialog_data["filters"]
    del filters["category_id"]


async def _process_delete_title(_: CallbackQuery, __: Button, manager: DialogManager):
    filters = manager.dialog_data["filters"]
    del filters["title"]


async def _process_delete_file_types(_: CallbackQuery, __: Button, manager: DialogManager):
    filters = manager.dialog_data["filters"]
    del filters["file_types"]
    await manager.find(SELECT_FILE_TYPES_ID).reset_checked()


def file_types_names(data: dict) -> list[str]:
    return [
        get_file_type_name(ft)
        for ft in data["dialog_data"]["filters"]["file_types"]
    ]


_filters = F["dialog_data"]["filters"]

file_list_dialog = Dialog(
    Window(
        Case(
            {
                0: Const("Фильтры не установлены"),
                None: Const("Фильтры не установлены"),
                ...: Multi(
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
            },
            selector=_filters.len() or 0
        ),
        Row(
            Start(
                Const("🗂 Категория"),
                state=CategoryFindSG.main,
                id="category"
            ),
            Button(
                Const("❌"),
                id="del_category",
                on_click=_process_delete_category,
                when=_filters["category_id"]
            ),
        ),
        Row(
            SwitchTo(
                Const("🏷 Тип файла"),
                state=FileListSG.input_file_type,
                id="file_types"
            ),
            Button(
                Const("❌"),
                id="del_file_types",
                on_click=_process_delete_file_types,
                when=_filters["file_types"]
            ),
        ),

        Row(
            SwitchTo(
                Const("📃 Название файла"),
                state=FileListSG.input_file_title,
                id="file_title"
            ),
            Button(
                Const("❌"),
                id="del_title",
                on_click=_process_delete_title,
                when=_filters["title"]
            ),
        ),

        SwitchTo(
            Const("🔎 Поиск"),
            state=FileListSG.file_list,
            id="find_files",
        ),
        state=FileListSG.main,
        getter=_main_window_getter,
    ),

    Window(
        Const("Выберите тип файла"),
        Group(
            Multiselect(
                Format("✓ {item.name}"),
                Format("{item.name}"),
                id=SELECT_FILE_TYPES_ID,
                type_factory=str_to_file_type,
                on_state_changed=_process_state_file_type,
                item_id_getter=lambda file_type: file_type.value,
                items="file_types",
            ),
            width=1,
        ),
        Back(BACK_TEXT_RU),
        state=FileListSG.input_file_type,
        getter={
            "file_types": [
                FileTypeItem(name=name, value=ft)
                for name, ft in file_types_with_names()
            ]
        },
    ),
    Window(
        Const("Введите часть названия файлов"),
        MessageInput(
            _process_input_title,
            content_types=ContentType.TEXT,
        ),
        BackTo(FileListSG.main, BACK_TEXT_RU),
        state=FileListSG.input_file_title,
    ),

    Window(
        Const("Выберите файл из списка"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="select_file",
                type_factory=int,
                on_click=_process_click_file,
                item_id_getter=lambda file: file.id,
                items="files",
            ),
            id="file_list",
            width=1,
            height=7
        ),
        BackTo(FileListSG.main, BACK_TEXT_RU),
        state=FileListSG.file_list,
        getter=_files_find_getter
    ),
    on_start=_on_start,
    on_process_result=_on_process_result
)
