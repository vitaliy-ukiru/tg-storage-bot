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

class TelegramIssuer(Issuer):
    def __init__(self, user_id: UserId):
        self._user_id = user_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    def can(self, op: Operation) -> bool:
        return True

    @property
    def issuer_type(self) -> IssuerType:
        return IssuerType.TELEGRAM


class ApiIssuer(Issuer):
    def __init__(self, token: TokenInfo):
        self._token = token

    @property
    def user_id(self) -> UserId:
        return self._token.user_id

    def can(self, op: Operation) -> bool:
        _OPERATION_TO_SCOPE = {
            Operation.category_create: Scope.category_create,
            Operation.category_edit: Scope.category_edit,
            Operation.file_create: Scope.file_create,
            Operation.file_edit: Scope.file_edit,
            Operation.file_delete: Scope.file_delete,
        }

        scope = _OPERATION_TO_SCOPE.get(op)
        if not scope:
            return False

        return scope in self._token.scopes

    @property
    def issuer_type(self) -> IssuerType:
        return IssuerType.TELEGRAM