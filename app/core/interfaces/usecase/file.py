__all__ = (
    'FileUsecase',
    'FileSaver', 'FileGetter', 'FileFinder', 'FileUpdater', 'FileDeleter',
)

from abc import abstractmethod
from typing import Protocol, Optional, overload, Literal

from app.core.domain.dto.common import Pagination
from app.core.interfaces.access import AccessController
from app.core.interfaces.repository.common import FilterField
from app.core.domain.dto.file import CreateFileDTO, FilesFindDTO, ReloadFileDTO
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import File, FileId
from app.core.domain.models.user import UserId


class FileSaver(Protocol):

    @abstractmethod
    async def save_file(self, dto: CreateFileDTO, access: AccessController) -> File:
        raise NotImplementedError


class FileGetter(Protocol):
    @abstractmethod
    async def get_file(self, file_id: FileId, access: AccessController) -> File:
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
        access: AccessController
    ) -> File:
        raise NotImplementedError

    @abstractmethod
    async def update_title(
        self,
        file_id: FileId,
        title: str,
        access: AccessController
    ) -> File:
        raise NotImplementedError

    @abstractmethod
    async def reload_file(
        self,
        file_id: FileId,
        dto: ReloadFileDTO,
        access: AccessController
    ) -> File:
        raise NotImplementedError


class FileDeleter(Protocol):
    @abstractmethod
    async def delete_file(self, file_id: FileId, access: AccessController):
        raise NotImplementedError


class FileUsecase(
    FileSaver, FileGetter,
    FileFinder, FileUpdater, FileDeleter
):
    pass
