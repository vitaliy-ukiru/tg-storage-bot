from typing import Optional

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Back, Button, SwitchTo
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Text, Const

BACK_TEXT = Const("Назад")


class BackTo(SwitchTo):
    def __init__(self,
                 state: State,
                 text: Text = BACK_TEXT,
                 id: str = "__back_to__",
                 on_click: Optional[OnClick] = None,
                 when: WhenCondition = None):
        super().__init__(text=text, id=id, state=state, on_click=on_click, when=when)
        self.state = state
