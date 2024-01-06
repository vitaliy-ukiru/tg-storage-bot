__all__ = (
    'WidgetDataObjectABC',

)

from abc import abstractmethod
from typing import Generic, TypeVar

from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.common import ManagedWidget

from ..base import (ManagerGetterProvider, ManagerFieldProvider,
                                      DialogManagerFieldProvider, ManagedDataObject, ManagerProviderVariant,
                                      get_manager)

T = TypeVar('T')

ProviderT = TypeVar('ProviderT',
                    ManagerGetterProvider,
                    ManagerFieldProvider,
                    DialogManagerFieldProvider)

ManagedWidgetT = TypeVar("ManagedWidgetT", bound=ManagedWidget)


class WidgetDataObjectABC(Generic[T, ManagedWidgetT], ManagedDataObject[T]):
    def __init__(self, widget_id: str):
        self._widget_id = widget_id

    @abstractmethod
    def process_get(self, widget: ManagedWidgetT):
        raise NotImplementedError

    @abstractmethod
    def process_set(self, widget: ManagedWidgetT, value: T):
        raise NotImplementedError

    @abstractmethod
    def process_del(self, widget: ManagedWidgetT):
        raise NotImplementedError

    def prepare_args(self, obj: ManagerProviderVariant):
        manager = get_manager(obj)
        widget = self._get_widget(manager)
        return (widget,)

    @property
    def widget_id(self) -> str:
        return self._widget_id

    def _get_widget(self, m: DialogManager) -> ManagedWidget[T]:
        w = m.find(self._widget_id)
        if w is None:
            raise ValueError(f"Fail find widget {self._widget_id!r} in manager {m!r}")
        return w
