__all__ = (
    'FileSaver',
    'FileGetter',
    'FileFinder',
    'FileUpdater',
    'FileDeleter',
)

from abc import abstractmethod
from typing import Protocol, Sequence, Optional

from app.core.domain.dto.common import Pagination
from app.core.domain.models.file import File, FileId
from app.core.interfaces.repository.common import FilterField


class FileSaver(Protocol):
    @abstractmethod
    async def save_file(self, file: File) -> FileId:
        raise NotImplementedError


class FileGetter(Protocol):
    @abstractmethod
    async def get_file(self, file_id: FileId) -> File:
        raise NotImplementedError


class FileFinder(Protocol):
    @abstractmethod
    async def find_files(self, filters: Sequence[FilterField],
                         paginate: Optional[Pagination] = None) -> list[File]:
        raise NotImplementedError

    @abstractmethod
    async def get_files_count(self, filters: Sequence[FilterField]) -> int:
        raise NotImplementedError


class FileUpdater(Protocol):
    @abstractmethod
    async def update_file(self, file: File):
        raise NotImplementedError


class FileDeleter(Protocol):
    @abstractmethod
    async def delete_file(self, file_id: FileId):
        raise NotImplementedError
