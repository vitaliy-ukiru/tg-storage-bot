__all__ = (
    'DialogDataProp',
)

from typing import TypeVar

from aiogram_dialog import DialogManager

from .base import ManagedDataObject, ManagerGetterProvider, get_manager, ManagerProviderVariant

T = TypeVar('T')


class DialogDataProp(ManagedDataObject[T]):
    def __init__(self, key: str):
        self.__key = key

    def process_get(self, manager: DialogManager):
        return manager.dialog_data.get(self.__key)

    def process_set(self, manager: DialogManager, value: T):
        manager.dialog_data[self.__key] = value

    def process_del(self, manager: DialogManager):
        del manager.dialog_data[self.__key]
