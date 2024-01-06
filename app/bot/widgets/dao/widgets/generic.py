__all__ = (
    'WidgetProperty',
    'WidgetGetter',
    'WidgetSetter',
    'WidgetDeleter'
)

from typing import TypeVar, TypeAlias, NoReturn, Callable, Self

from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.common import ManagedWidget
from app.bot.widgets.dao.base import (ManagerGetterProvider, ManagerFieldProvider,
                                      DialogManagerFieldProvider, ManagerProviderVariant, get_manager)
from .base import WidgetDataObjectABC

T = TypeVar('T')

ProviderT = TypeVar('ProviderT',
                    ManagerGetterProvider,
                    ManagerFieldProvider,
                    DialogManagerFieldProvider)

W = TypeVar("W", bound=Widget)

WidgetGetter: TypeAlias = Callable[[ProviderT, ManagedWidget[W]], T | None]
WidgetSetter: TypeAlias = Callable[[ProviderT, ManagedWidget[W], T], NoReturn]
WidgetDeleter: TypeAlias = Callable[[ProviderT, ManagedWidget[W]], NoReturn]


class WidgetProperty(WidgetDataObjectABC[T, W]):
    """
    WidgetProp it like builtin property, but it also provides widget object to functions
    Example:

        class Proxy:
            def get_dialog_manager(self):
                return self._manager

            @WidgetProperty("title_input")
            def title(self, widget):
                return widget.get_value()

            @title.setter
            def title(self, widget, value: str):  # noqa
                widget.set_value(value)

            @title.deleter
            def title(self, widget):  # noqa
                widget.set_value(None)

    """

    def __init__(self,
                 widget_id: str,
                 getter: WidgetGetter | None = None,
                 setter: WidgetSetter | None = None,
                 deleter: WidgetDeleter | None = None,
                 doc=None):
        super().__init__(widget_id)
        self.__get = getter
        self.__set = setter
        self.__del = deleter

        if doc is None and getter is not None:
            doc = getter.__doc__
        self.__doc__ = doc

    def __call__(self, getter: WidgetGetter) -> Self:
        return self.getter(getter)

    def __get__(self, obj: ManagerProviderVariant, owner=None):
        if self.__get is None:
            raise AttributeError(f"Widget {self._widget_id} is has no getter")
        return super().__get__(obj, owner)

    def __set__(self, obj: ManagerProviderVariant, value: T):
        if self.__set is None:
            raise AttributeError(f"Widget {self._widget_id} is read only")
        super().__set__(obj, value)

    def __delete__(self, obj: ManagerProviderVariant):
        if self.__set is None:
            raise AttributeError(f"Widget {self._widget_id} has no deleter")
        super().__delete__(obj)

    def prepare_args(self, obj: ManagerProviderVariant):
        manager = get_manager(obj)
        return (
            self._get_widget(manager), obj
        )

    def process_get(self, widget: ManagedWidget[W], obj: ManagerProviderVariant):
        return self.__get(obj, widget)

    def process_set(self, widget: ManagedWidget[W], obj: ManagerProviderVariant, value: T):
        self.__set(obj, widget, value)

    def process_del(self, widget: ManagedWidget[W], obj: ManagerProviderVariant):
        self.__del(obj, widget)

    def getter(self, getter: WidgetGetter) -> Self:
        return type(self)(self._widget_id, getter, self.__set, self.__del, self.__doc__)

    def setter(self, setter: WidgetSetter) -> Self:
        return type(self)(self._widget_id, self.__get, setter, self.__del, self.__doc__)

    def deleter(self, deleter: WidgetDeleter) -> Self:
        return type(self)(self._widget_id, self.__get, self.__set, deleter, self.__doc__)
