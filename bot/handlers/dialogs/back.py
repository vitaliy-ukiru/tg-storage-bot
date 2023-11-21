from typing import Optional

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Text, Const


BACK_TEXT = Const("Назад")

class BackTo(Back):

    def __init__(self,
                 state: State,
                 text: Text = BACK_TEXT,
                 id: str = "__back_to__",
                 on_click: Optional[OnClick] = None,
                 when: WhenCondition = None):
        super().__init__(text, id, on_click, when)
        self.state = state

    async def _on_click(
        self, callback: CallbackQuery, button: Button,
        manager: DialogManager,
    ):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)

            await manager.switch_to(self.state)
