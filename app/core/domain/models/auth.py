from abc import ABC, abstractmethod
from enum import StrEnum, auto

from .token import TokenInfo, Scope
from .user import UserId


class Operation(StrEnum):
    category_create = auto()
    category_edit = auto()

    file_create = auto()
    file_edit = auto()
    file_delete = auto()

    token_create = auto()
    token_delete = auto()


class IssuerType(StrEnum):
    UNKNOWN = auto()
    TELEGRAM = auto()
    API = auto()


class Issuer(ABC):
    @property
    @abstractmethod
    def user_id(self) -> UserId:
        raise NotImplementedError

    @abstractmethod
    def can(self, op: Operation) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def issuer_type(self) -> IssuerType:
        return IssuerType.UNKNOWN
