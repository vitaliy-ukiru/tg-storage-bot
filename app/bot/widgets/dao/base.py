__all__ = (
    'ManagedDataObject',
    'ManagerGetterProvider',
    'ManagerFieldProvider',
    'DialogManagerFieldProvider',
    'ManagerProviderVariant',
    'get_manager'
)

from abc import abstractmethod, ABC
from typing import TypeAlias, Protocol, runtime_checkable, Generic, TypeVar

from aiogram_dialog import DialogManager


@runtime_checkable
class ManagerGetterProvider(Protocol):
    @abstractmethod
    def get_dialog_manager(self) -> DialogManager:
        raise NotImplementedError


@runtime_checkable
class ManagerFieldProvider(Protocol):
    @property
    @abstractmethod
    def manager(self) -> DialogManager:
        raise NotImplementedError


@runtime_checkable
class DialogManagerFieldProvider(Protocol):
    @property
    @abstractmethod
    def dialog_manager(self) -> DialogManager:
        raise NotImplementedError


ManagerProviderVariant: TypeAlias = (ManagerGetterProvider |
                                     DialogManagerFieldProvider |
                                     ManagerFieldProvider)


def get_manager(provider: ManagerProviderVariant) -> DialogManager:
    if isinstance(provider, ManagerGetterProvider):
        return provider.get_dialog_manager()

    if isinstance(provider, DialogManagerFieldProvider):
        return provider.dialog_manager

    if isinstance(provider, ManagerFieldProvider):
        return provider.manager

    raise TypeError(f'Object {type(provider).__name__} dont implement ManagerProviderVariant')


T = TypeVar('T')


class DataObjectABC(ABC, Generic[T]):
    @abstractmethod
    def __get__(self, obj: ManagerProviderVariant, owner=None):
        raise NotImplementedError

    @abstractmethod
    def __set__(self, obj: ManagerProviderVariant, value: T):
        raise NotImplementedError

    @abstractmethod
    def __delete__(self, obj: ManagerProviderVariant):
        raise NotImplementedError


class ManagedDataObject(ABC, Generic[T]):
    @abstractmethod
    def process_get(self, manager: DialogManager) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def process_set(self, manager: DialogManager, value: T):
        raise NotImplementedError

    @abstractmethod
    def process_del(self, manager: DialogManager):
        raise NotImplementedError

    def __get__(self, obj: ManagerProviderVariant, owner=None) -> T | None:
        manager = get_manager(obj)
        return self.process_get(manager)

    def __set__(self, obj: ManagerProviderVariant, value: T):
        manager = get_manager(obj)
        self.process_set(manager, value)

    def __delete__(self, obj: ManagerProviderVariant):
        manager = get_manager(obj)
        self.process_del(manager)
