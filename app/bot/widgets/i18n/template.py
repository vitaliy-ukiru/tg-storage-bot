from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_i18n import I18nContext

from app.bot.widgets.i18n import KeyJoiner

I18N_KEY = "i18n"


class Template(Text):
    def __init__(self, key: str | KeyJoiner, default_text: Text = None, when: WhenCondition = None):
        super().__init__(when)
        if isinstance(key, KeyJoiner):
            key = key()

        self.key = key
        self.default_text = default_text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        i18n: I18nContext | None = manager.middleware_data.get(I18N_KEY)
        if i18n is None:
            if self.default_text is not None:
                return await self.default_text._render_text(data, manager)

            return f'<fail get translator>: {self.key}'

        return i18n.get(self.key)
