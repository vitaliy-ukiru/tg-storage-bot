from operator import itemgetter
from typing import Dict, Self, Callable, Union, Awaitable

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_i18n import I18nContext

I18N_KEY = "i18n"

ParamsGetter = Callable[[dict], dict]
ParamsGetterVariant = Union[ParamsGetter, dict, None]


def _get_identity(params: dict) -> ParamsGetter:
    def identity(_) -> Dict:
        return params

    return identity


def get_params_getter(attr_val: ParamsGetterVariant) -> ParamsGetter:
    if isinstance(attr_val, Callable):
        return attr_val
    elif attr_val is None:
        return _get_identity({})
    else:
        return _get_identity(attr_val)


class Template(Text):
    def __init__(
        self,
        key: Union[str, "TemplateProxy"],
        default_text: Text | None = None,
        getter: ParamsGetterVariant = None,
        when: WhenCondition = None
    ):
        super().__init__(when)
        if not isinstance(key, str):
            key = str(key)

        self.key = key
        self.default_text = default_text
        self.getter = get_params_getter(getter)

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        i18n: I18nContext | None = manager.middleware_data.get(I18N_KEY)
        if i18n is None:
            if self.default_text is not None:
                return await self.default_text.render_text(data, manager)

            return f'<fail get translator>: {self.key}'

        params = self.getter(data)
        return i18n.get(self.key, **params)


class TemplateProxy:
    __key_separator: str
    __query: tuple[str, ...]

    def __init__(self, *parts: str, key_separator: str = "-", ) -> None:
        self.__key_separator = key_separator
        self.__query = parts

    def __getattr__(self, item: str) -> Self:
        query = self.__query + (item,)
        return TemplateProxy(*query, key_separator=self.__key_separator)

    def __call__(self,
                 default_text: Text = None,
                 getter: ParamsGetterVariant = None,
                 when: WhenCondition = None,
                 ) -> Template:
        return self.get_template(default_text, getter, when)

    def __str__(self):
        return self.get_key()

    def get_key(self) -> str:
        return self.__key_separator.join(self.__query)

    def get_template(self,
                     default_text: Text = None,
                     getter: ParamsGetterVariant = None,
                     when: WhenCondition = None,
                     ) -> Template:
        return Template(self.get_key(), default_text=default_text, getter=getter, when=when)
