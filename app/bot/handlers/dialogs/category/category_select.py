from typing import Any

from aiogram_dialog import Dialog, Window, Data, DialogManager
from aiogram_dialog.widgets.kbd import Column, Start

from app.bot.states.dialogs import CategoryFindSG, CategorySelectSG, CategoryCreateSG
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import TL, CancelI18n

tl = TL.category.select

async def _process_result(_: Data, result: Any, manager: DialogManager):
    if result:
        await manager.done(dict(category_id=result["category_id"]))


category_select_dialog = Dialog(
    Window(
        tl.target(),
        Column(
            Start(
                Emoji("🔎", tl.btn.exists()),
                id="category_exists",
                state=CategoryFindSG.main,
            ),
            Start(
                Emoji("🆕", tl.btn.create()),
                id="category_create",
                state=CategoryCreateSG.input_title
            ),
            CancelI18n()
        ),
        state=CategorySelectSG.start,
    ),
    on_process_result=_process_result
)
