from typing import Optional, Any

from aiogram.fsm.state import State
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Back, Cancel
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Text

from app.bot.widgets import BackTo
from app.bot.widgets.emoji import Emoji
from app.bot.widgets.i18n import Template

BACK_TEXT = Emoji("⬅", Template('common-btn-back'))
CANCEL_TEXT = Emoji("✖", Template('common-btn-cancel'))
CLOSE_TEXT = Template('common-btn-close')


class BackI18n(Back):
    def __init__(self,
                 text: Text = BACK_TEXT,
                 id: str = "__back__",
                 on_click: Optional[OnClick] = None,
                 when: WhenCondition = None):
        super().__init__(text, id, on_click, when)


class CancelI18n(Cancel):
    def __init__(self,
                 text: Text = CANCEL_TEXT,
                 id: str = "__cancel__",
                 result: Any = None,
                 on_click: Optional[OnClick] = None,
                 when: WhenCondition = None):
        super().__init__(text, id, result, on_click, when)


class CloseI18n(Cancel):
    def __init__(self,
                 text: Text = CLOSE_TEXT,
                 id: str = "__close__",
                 result: Any = None,
                 on_click: Optional[OnClick] = None,
                 when: WhenCondition = None):
        super().__init__(text, id, result, on_click, when)



class BackToI18n(BackTo):
    def __init__(self,
                 state: State,
                 text: Text = BACK_TEXT,
                 id: str = "__back_to__",
                 on_click: Optional[OnClick] = None,
                 when: WhenCondition = None):
        super().__init__(state, text, id, on_click, when)
