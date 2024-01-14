__all__ = (
    'FileUsecase',
)

from abc import abstractmethod
from typing import Protocol, Optional, overload, Literal

from app.core.domain.dto.common import Pagination
from app.core.interfaces.repository.common import FilterField
from app.core.domain.dto.file import CreateFileDTO, FilesFindDTO, ReloadFileDTO
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import File, FileId
from app.core.domain.models.user import UserId


class FileUsecase(Protocol):

    @abstractmethod
    async def save_file(self, dto: CreateFileDTO) -> File:
        raise NotImplementedError

    @abstractmethod
    async def get_file(self, file_id: FileId, user_id: Optional[UserId] = None) -> File:
        raise NotImplementedError

    @abstractmethod
    async def set_category(self, file_id: FileId, category_id: CategoryId, user_id: UserId) -> File:
        raise NotImplementedError

    @abstractmethod
    async def update_title(self, file_id: FileId, title: str, user_id: UserId) -> File:
        raise NotImplementedError

    @abstractmethod
    async def reload_file(self, file_id: FileId, dto: ReloadFileDTO, user_id: UserId) -> File:
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, file_id: FileId, user_id: UserId):
        raise NotImplementedError

    @overload
    async def find_files(
        self,
        *filters: FilterField,
        dto: Optional[FilesFindDTO] = None,
        paginate: Optional[Pagination] = None,
        total_count: Literal[True]
    ) -> tuple[list[File], int]:
        raise NotImplementedError

    @overload
    async def find_files(
        self,
        *filters: FilterField,
        dto: Optional[FilesFindDTO] = None,
        paginate: Optional[Pagination] = None,
        total_count: Literal[False]
    ) -> list[File]:
        raise NotImplementedError

    @overload
    async def find_files(
        self,
        *filters: FilterField,
        dto: Optional[FilesFindDTO] = None,
        paginate: Optional[Pagination] = None,
        total_count: Optional[bool] = None
    ) -> list[File] | tuple[list[File], int]:
        raise NotImplementedError

    @abstractmethod
    async def find_files(
        self,
        *filters: FilterField,
        dto: Optional[FilesFindDTO] = None,
        paginate: Optional[Pagination] = None,
        total_count: Optional[bool] = None
    ) -> tuple[list[File], int] | list[File]:
        raise NotImplementedError
