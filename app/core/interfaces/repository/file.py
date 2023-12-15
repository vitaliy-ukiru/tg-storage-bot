__all__ = (
    'FileRepository',
    'FilterField',
)

import abc
from dataclasses import dataclass
from typing import TypeVar, Generic, Protocol, Sequence

from app.core.domain.models.file import File, FileId

T = TypeVar("T")


@dataclass(frozen=True)
class FilterField(Generic[T]):
    name: str
    value: T


class FileRepository(Protocol):
    @abc.abstractmethod
    async def save_file(self, file: File) -> FileId:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_file(self, file_id: FileId) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_files(self, filters: Sequence[FilterField]) -> list[File]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_file(self, file: File):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_file(self, file_id: FileId):
        raise NotImplementedError
