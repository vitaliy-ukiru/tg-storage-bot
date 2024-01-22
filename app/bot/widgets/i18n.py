from typing import Any, Dict, Protocol, TypeAlias, List, Self, Tuple

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_i18n import I18nContext

I18N_KEY = "i18n"


class KeyJoiner:
    key_separator: str
    _query: tuple[str, ...]

    def __init__(self, *parts: str, key_separator: str = "-", ) -> None:
        self.key_separator = key_separator
        self._query = parts

    def __getattr__(self, item: str) -> Self:
        query = self._query + (item,)
        return KeyJoiner(*query, key_separator=self.key_separator)

    def __call__(self) -> str:
        return self.key_separator.join(self._query)


class Template(Text):
    def __init__(self, key: str | KeyJoiner, default_text: str = None, when: WhenCondition = None):
        super().__init__(when)
        if isinstance(key, KeyJoiner):
            key = key()

        self.key = key
        self.default_text = default_text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        i18n: I18nContext | None = manager.middleware_data.get(I18N_KEY)
        if i18n is None:
            if self.default_text is not None:
                return self.default_text.format_map(data)

            return f'<fail get translator>: {self.key}'

        return i18n.get(self.key)
