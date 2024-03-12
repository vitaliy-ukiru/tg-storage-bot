from abc import abstractmethod
from enum import StrEnum, auto
from typing import Protocol

from app.web_api.models.auth import Scope
from app.core.domain.models.category import Category
from app.core.domain.models.file import File
from app.core.domain.models.user import UserId


class Operation(StrEnum):
    category_create = auto()
    category_edit = auto()
    file_create = auto()
    file_edit = auto()
    file_delete = auto()


class AccessController(Protocol):
    @abstractmethod
    def ensure_have_access(self, op: Operation):
        raise NotImplementedError

    @abstractmethod
    def ensure_own_category(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def ensure_own_file(self, file: File):
        raise NotImplementedError

    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
