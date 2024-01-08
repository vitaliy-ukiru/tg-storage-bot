from typing import TypeVar

from aiogram_dialog.widgets.input import ManagedTextInput

from .base import WidgetDataObjectABC

T = TypeVar('T')


class TextInputProp(WidgetDataObjectABC[T, ManagedTextInput[T]]):
    def get(self, widget: ManagedTextInput[T]) -> T:  # noqa
        return widget.get_value()

    def set(self, widget: ManagedTextInput[T], value: T):  # noqa
        widget.widget.set_widget_data(widget.manager, str(value))

    def delete(self, widget: ManagedTextInput[T]):  # noqa
        widget.widget.set_widget_data(widget.manager, None)
