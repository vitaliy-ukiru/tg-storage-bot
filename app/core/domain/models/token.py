from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto

from .user import User, UserId


class ScopeEnumType(StrEnum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower().replace("_", ":", 1)


class Scope(ScopeEnumType):
    category_create = auto()  # = "category:create"
    category_edit = auto()  # = "category:edit"
    file_create = auto()  # = "file:create"
    file_edit = auto()  # = "file:edit"
    file_delete = auto()  # = "file:delete"


@dataclass
class Token:
    id: str
    user_id: UserId

    @property
    def token(self) -> str:
        return f'{self.user_id}:{self.id}'


@dataclass
class TokenInfo(Token):
    name: str
    scopes: set[Scope]
    expiry: datetime | None

    @property
    def expired(self):
        return self.expiry <= datetime.now()
