from operator import itemgetter
from typing import Dict, Any, Union, Callable

from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Case, Text
from aiogram_dialog.widgets.text.multi import Selector
from magic_filter import MagicFilter

from .template import ParamsGetterVariant, Template


def _magic_filter_field(f: MagicFilter):
    def _getter(data):
        return f.resolve(data)

    return _getter


def _file_id_getter(value_getter: Callable[[dict], ...]):
    def _getter(data: Dict):
        return {
            "file_id": value_getter(data)
        }

    return _getter


def ensure_file_id_getter(field_getter: str | MagicFilter):
    if isinstance(field_getter, str):
        field_getter = itemgetter(field_getter)
    elif isinstance(field_getter, MagicFilter):
        field_getter = _magic_filter_field(field_getter)

    return _file_id_getter(field_getter)

class FileTitle(Case):
    def __init__(self, title: Text, file_id_field: str | MagicFilter,
                 selector: Union[str, Selector, MagicFilter],
                 default_locale_text: Text = None,
                 when: WhenCondition = None, ):
        file_id_getter = ensure_file_id_getter(file_id_field)
        super().__init__(
            texts={
                ...: title,
                None: Template(
                    'file-title',
                    default_text=default_locale_text,
                    getter=file_id_getter
                )

            },
            selector=selector,
            when=when,
        )
