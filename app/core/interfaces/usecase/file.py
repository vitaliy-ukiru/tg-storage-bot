__all__ = (
    'FileUsecase',
    'FileSaver', 'FileGetter', 'FileFinder', 'FileUpdater', 'FileDeleter',
)

from abc import abstractmethod
from typing import Protocol, Optional, overload, Literal

from app.core.domain.dto.common import Pagination
from app.core.domain.dto.file import CreateFileDTO, FilesFindDTO, ReloadFileDTO
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import File, FileId
from app.core.domain.models.auth import Issuer


class FileSaver(Protocol):

    @abstractmethod
    async def save_file(self, dto: CreateFileDTO, issuer: Issuer) -> File:
        raise NotImplementedError


class FileGetter(Protocol):
    @abstractmethod
    async def get_file(self, file_id: FileId, issuer: Issuer) -> File:
        raise NotImplementedError


# noinspection PyProtocol
class FileFinder(Protocol):
    @overload
    async def find_files(
        self,
        dto: FilesFindDTO,
        total_count: Literal[True],
        paginate: Optional[Pagination] = None,
    ) -> tuple[list[File], int]:
        raise NotImplementedError

    @overload
    async def find_files(
        self,
        dto: FilesFindDTO,
        paginate: Optional[Pagination] = None,
    ) -> list[File]:
        raise NotImplementedError

    @abstractmethod
    async def find_files(
        self,
        dto: FilesFindDTO,
        paginate: Optional[Pagination] = None,
        total_count: Optional[bool] = None
    ) -> tuple[list[File], int] | list[File]:
        raise NotImplementedError


class FileUpdater(Protocol):
    @abstractmethod
    async def set_category(
        self,
        file_id: FileId,
        category_id: CategoryId,
        issuer: Issuer
    ) -> File:
        raise NotImplementedError

    @abstractmethod
    async def update_title(
        self,
        file_id: FileId,
        title: str,
        issuer: Issuer
    ) -> File:
        raise NotImplementedError

    @abstractmethod
    async def reload_file(
        self,
        file_id: FileId,
        dto: ReloadFileDTO,
        issuer: Issuer
    ) -> File:
        raise NotImplementedError


class FileDeleter(Protocol):
    @abstractmethod
    async def delete_file(self, file_id: FileId, issuer: Issuer):
        raise NotImplementedError


class FileUsecase(
    FileSaver, FileGetter,
    FileFinder, FileUpdater, FileDeleter
):
    pass
