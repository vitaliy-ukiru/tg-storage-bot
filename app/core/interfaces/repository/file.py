__all__ = (
    'FileRepository',
)

import abc
from typing import Protocol, Sequence

from app.core.domain.models.file import File, FileId
from app.core.interfaces.repository.common import FilterField


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
