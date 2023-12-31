__all__ = (
    'FileUsecase',
)
import abc
from typing import Protocol, Optional

from app.core.domain.dto.common import Pagination
from app.core.interfaces.repository.common import FilterField
from app.core.domain.dto.file import CreateFileDTO, FilesFindDTO, ReloadFileDTO
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import File, FileId
from app.core.domain.models.user import UserId


class FileUsecase(Protocol):

    @abc.abstractmethod
    async def save_file(self, dto: CreateFileDTO) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_file(self, file_id: FileId, user_id: UserId = None) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def find_files(self,
                         *filters: FilterField,
                         dto: FilesFindDTO = None,
                         paginate: Optional[Pagination] = None,
                         total_count: bool = False) -> tuple[list[File], Optional[int]]:
        raise NotImplementedError

    @abc.abstractmethod
    async def set_category(self, file_id: FileId, category_id: CategoryId, user_id: UserId) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_title(self, file_id: FileId, title: str, user_id: UserId) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def reload_file(self, file_id: FileId, dto: ReloadFileDTO, user_id: UserId) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_file(self, file_id: FileId, user_id: UserId):
        raise NotImplementedError
