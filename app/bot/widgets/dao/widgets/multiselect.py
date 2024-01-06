__all__ = (
    'MultiselectProp',
    'MultiselectObjectProxy'
)

from typing import TypeVar, Generic, Sequence

from aiogram_dialog.widgets.kbd import ManagedMultiselect, Multiselect

from .base import WidgetDataObjectABC, ManagedWidgetT
from ..base import ManagerProviderVariant

T = TypeVar('T')


class MultiselectObjectProxy(Generic[T]):
    def __init__(self, widget: ManagedMultiselect[T]):
        self._widget = widget

    @property
    def widget(self) -> ManagedMultiselect[T]:
        return self._widget

    @property
    def items(self) -> Sequence[T] | None:
        items = self._widget.get_checked()
        if len(items) == 0:
            return None
        return items

    async def set(self, item_id: T, checked=False):
        await self._widget.set_checked(item_id, checked)

    async def enable(self, item_id: T):
        await self._widget.set_checked(item_id, True)

    async def disable(self, item_id: T):
        await self._widget.set_checked(item_id, False)

    async def setup(self, items: Sequence[T]):
        for item in items:
            await self.enable(item)

    async def delete(self):
        await self._widget.reset_checked()


class MultiselectProp(WidgetDataObjectABC[T, ManagedMultiselect[T]]):

    @staticmethod
    def process_get(widget: ManagedMultiselect[T]):
        return MultiselectObjectProxy(widget)

    def process_set(self, widget: ManagedMultiselect[T], value: T):
        raise AttributeError(f"Multiselect DAO setter in async, use async method set in proxy (getter)")

    def process_del(self, widget: ManagedMultiselect[T]):
        raise AttributeError(f"Multiselect DAO deleter in async, use async method delete (getter)")
