from typing import Optional

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Data, StartMode
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Start, Button
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.utils import GetterVariant, ensure_data_getter


class StartWithData(Start):

    def __init__(self,
                 text: Text,
                 id: str,
                 state: State,
                 data: Data = None,
                 on_click: Optional[OnClick] = None,
                 getter: GetterVariant = None,
                 mode: StartMode = StartMode.NORMAL,
                 when: WhenCondition = None):
        self.getter = ensure_data_getter(getter)
        super().__init__(text, id, state, data, on_click, mode, when)

    async def _on_click(self, callback: CallbackQuery, button: Button, manager: DialogManager):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)
        current_data = await self.getter(**manager.middleware_data)
        start_data = self.start_data or {}
        await manager.start(self.state, start_data | current_data, self.mode)
