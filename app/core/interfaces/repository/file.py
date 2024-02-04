__all__ = (
    'FileRepoSaver',
    'FileRepoGetter',
    'FileRepoFinder',
    'FileRepoUpdater',
    'FileRepoDeleter',
)

from abc import abstractmethod
from typing import Protocol, Sequence, Optional

from app.core.domain.dto.common import Pagination
from app.core.domain.models.file import File, FileId
from app.core.interfaces.repository.common import FilterField


class FileRepoSaver(Protocol):
    @abstractmethod
    async def save_file(self, file: File) -> FileId:
        raise NotImplementedError


class FileRepoGetter(Protocol):
    @abstractmethod
    async def get_file(self, file_id: FileId) -> File:
        raise NotImplementedError


class FileRepoFinder(Protocol):
    @abstractmethod
    async def find_files(self, filters: Sequence[FilterField],
                         paginate: Optional[Pagination] = None) -> list[File]:
        raise NotImplementedError

    @abstractmethod
    async def get_files_count(self, filters: Sequence[FilterField]) -> int:
        raise NotImplementedError


class FileRepoUpdater(Protocol):
    @abstractmethod
    async def update_file(self, file: File):
        raise NotImplementedError


class FileRepoDeleter(Protocol):
    @abstractmethod
    async def delete_file(self, file_id: FileId):
        raise NotImplementedError
