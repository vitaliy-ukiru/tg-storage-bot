from typing import Optional

from aiogram.fsm.state import State
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.kbd.state import BACK_TEXT as _BACK_TEXT
from aiogram_dialog.widgets.text import Text, Const

BACK_TEXT = Const("⬅ Назад")
CANCEL_TEXT = Const("✖ Отмена")
CLOSE_TEXT = Const("Закрыть")

class BackTo(SwitchTo):
    def __init__(self,
                 state: State,
                 text: Text = _BACK_TEXT,
                 id: str = "__back_to__",
                 on_click: Optional[OnClick] = None,
                 when: WhenCondition = None):
        super().__init__(text=text, id=id, state=state, on_click=on_click, when=when)
        self.state = state
