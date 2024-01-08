__all__ = (
    'DialogDataProp',
    'DialogDataRequiredProp'
)

from typing import Generic, TypeVar

from aiogram_dialog import DialogManager

from .base import ManagedDataObject

T = TypeVar('T')


class DialogDataProp(ManagedDataObject[T]):
    def __init__(self, key: str):
        self._key = key

    def get(self, manager: DialogManager):
        return manager.dialog_data.get(self._key)

    def set(self, manager: DialogManager, value):
        manager.dialog_data[self._key] = value

    def delete(self, manager: DialogManager):
        del manager.dialog_data[self._key]


class DialogDataRequiredProp(DialogDataProp[T]):
    def get(self, manager: DialogManager):
        return manager.dialog_data[self._key]
