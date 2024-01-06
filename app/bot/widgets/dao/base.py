__all__ = (
    'DataObjectABC',
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


class ManagedDataObject(DataObjectABC[T]):

    @abstractmethod
    def process_get(self, manager: DialogManager):
        raise NotImplementedError

    @abstractmethod
    def process_set(self, manager: DialogManager, value: T):
        raise NotImplementedError

    @abstractmethod
    def process_del(self, manager: DialogManager):
        raise NotImplementedError

    def prepare_args(self, obj: ManagerProviderVariant):
        return (get_manager(obj),)

    def __get__(self, obj: ManagerProviderVariant, owner=None):
        return self.process_get(*self.prepare_args(obj))

    def __set__(self, obj: ManagerProviderVariant, value: T):
        self.process_set(*self.prepare_args(obj), value)

    def __delete__(self, obj: ManagerProviderVariant):
        self.process_del(*self.prepare_args(obj))
