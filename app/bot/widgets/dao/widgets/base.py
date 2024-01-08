__all__ = (
    'WidgetDataObjectABC',

)

from abc import abstractmethod
from typing import Generic, TypeVar

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedWidget

from ..base import (ManagerGetterProvider, ManagerFieldProvider,
                    DialogManagerFieldProvider, ManagerProviderVariant,
                    get_manager, DataObjectABC)

T = TypeVar('T')

ProviderT = TypeVar('ProviderT',
                    ManagerGetterProvider,
                    ManagerFieldProvider,
                    DialogManagerFieldProvider)

ManagedWidgetT = TypeVar("ManagedWidgetT", bound=ManagedWidget)


class WidgetDataObjectABC(Generic[T, ManagedWidgetT], DataObjectABC[T]):
    def __init__(self, widget_id: str):
        self._widget_id = widget_id

    @abstractmethod
    def get(self, widget: ManagedWidgetT) -> T:
        raise NotImplementedError

    @abstractmethod
    def set(self, widget: ManagedWidgetT, value: T):
        raise NotImplementedError

    @abstractmethod
    def delete(self, widget: ManagedWidgetT):
        raise NotImplementedError

    @property
    def widget_id(self) -> str:
        return self._widget_id

    def _find_widget(self, m: DialogManager) -> ManagedWidgetT:
        w = m.find(self._widget_id)
        if w is None:
            raise ValueError(f"Fail find widget {self._widget_id!r} in manager {m!r}")
        return w

    def _get_widget(self, provider: ManagerProviderVariant) -> ManagedWidgetT:
        manager = get_manager(provider)
        return self._find_widget(manager)

    def __get__(self, obj: ManagerProviderVariant, owner=None) -> T:
        widget = self._get_widget(obj)
        return self.get(widget)

    def __set__(self, obj: ManagerProviderVariant, value: T):
        widget = self._get_widget(obj)
        self.set(widget, value)

    def __delete__(self, obj: ManagerProviderVariant):
        widget = self._get_widget(obj)
        self.delete(widget)
