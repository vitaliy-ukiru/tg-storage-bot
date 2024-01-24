
from typing import Dict, Self, Callable, Union

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_i18n import I18nContext


I18N_KEY = "i18n"


class Template(Text):
    def __init__(self, key: Union[str, "TemplateProxy"], default_text: Text = None, when: WhenCondition = None):
        super().__init__(when)
        if not isinstance(key, str):
            key = str(key)

        self.key = key
        self.default_text = default_text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        i18n: I18nContext | None = manager.middleware_data.get(I18N_KEY)
        if i18n is None:
            if self.default_text is not None:
                return await self.default_text._render_text(data, manager)

            return f'<fail get translator>: {self.key}'

        return i18n.get(self.key)

class TemplateProxy:
    __key_separator: str
    __query: tuple[str, ...]

    def __init__(self, *parts: str, key_separator: str = "-", ) -> None:
        self.__key_separator = key_separator
        self.__query = parts

    def __getattr__(self, item: str) -> Self:
        query = self.__query + (item,)
        return TemplateProxy(*query, key_separator=self.__key_separator)

    def __call__(self, default_text: Text = None, when: WhenCondition = None) -> Template:
        return self.get_template(default_text, when)

    def __str__(self):
        return self.get_key()

    def get_key(self) -> str:
        return self.__key_separator.join(self.__query)

    def get_template(self, default_text: Text = None, when: WhenCondition = None) -> Template:
        return Template(self.get_key(), default_text=default_text, when=when)
