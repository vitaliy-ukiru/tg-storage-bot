from typing import Any

from aiogram_dialog import Dialog, Window, Data, DialogManager
from aiogram_dialog.widgets.kbd import Column, Start, Cancel
from aiogram_dialog.widgets.text import Const

from app.bot.widgets import CANCEL_TEXT_RU
from app.bot.states.dialogs import CategoryFindSG, CategorySelectSG, CategoryCreateSG


async def _process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        await manager.done(dict(category_id=result["category_id"]))


category_select_dialog = Dialog(
    Window(
        Const("Выберите источник категории"),
        Column(
            Start(
                Const("🔎 Существующая"),
                id="category_exists",
                state=CategoryFindSG.main,
            ),
            Start(
                Const("🆕 Создать"),
                id="category_create",
                state=CategoryCreateSG.input_title
            ),
            Cancel(CANCEL_TEXT_RU)
        ),
        state=CategorySelectSG.start,
    ),
    on_process_result=_process_result
)
