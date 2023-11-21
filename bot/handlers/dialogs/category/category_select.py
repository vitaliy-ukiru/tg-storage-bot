from typing import Any

from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window, Data, DialogManager
from aiogram_dialog.widgets.kbd import Column, Start, Cancel
from aiogram_dialog.widgets.text import Const

from .category_create import CreateSG
from .find_category import FindSG


class SelectSG(StatesGroup):
    start = State()


async def _process_result(start_data: Data, result: Any, manager: DialogManager):
    if result:
        await manager.done(dict(category_id=result["category_id"]))


category_select_dialog = Dialog(
    Window(
        Const("Выберите источник категории"),
        Column(
            Start(
                Const("Существующая"),
                id="category_exists",
                state=FindSG.select_topic,
            ),
            Start(
                Const("Создать"),
                id="category_create",
                state=CreateSG.input_title
            ),
            Cancel()
        ),
        state=SelectSG.start,
    ),
    on_process_result=_process_result
)
