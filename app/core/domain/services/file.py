import abc
from dataclasses import asdict
from datetime import datetime
from typing import Protocol, Optional

from app.core.domain.dto.common import Pagination
from app.core.domain.dto.file import CreateFileDTO, ReloadFileDTO, FilesFindDTO
from app.core.domain.exceptions.category import CategoryViolation
from app.core.domain.exceptions.file import FileNotFound, FileAccessDenied
from app.core.domain.models.category import CategoryId, Category
from app.core.domain.models.file import File, FileId, RemoteFileId
from app.core.domain.models.user import UserId
from app.core.interfaces.repository.file import FileRepository
from app.core.interfaces.repository.common import FilterField
from app.core.interfaces.usecase.file import FileUsecase
from app.core.domain.services.internal.filter_merger import FilterMerger


class CategoryGetter(Protocol):
    @abc.abstractmethod
    async def get_category(self, category_id: CategoryId) -> Category:
        raise NotImplementedError


UNDEFINED_FILE_ID = FileId(0)


def _ensure_owner(file: File, user_id: UserId = None):
    if user_id is None:
        return

    if file.user_id != user_id:
        raise FileAccessDenied(file.id, user_id)


class FileService(FileUsecase):
    def __init__(self, repo: FileRepository, category_getter: CategoryGetter):
        self._repo = repo
        self._category_getter = category_getter

    async def save_file(self, dto: CreateFileDTO) -> File:
        file = File(
            UNDEFINED_FILE_ID,
            dto.title,
            dto.file_type,
            RemoteFileId(dto.remote_id),
            UserId(dto.user_id),
            datetime.now(),
        )

        if dto.category_id is not None:
            file.category = await self._category_getter.get_category(CategoryId(dto.category_id))

        file.id = await self._repo.save_file(file)
        return file

    async def get_file(self, file_id: FileId, user_id: UserId = None) -> File:
        file = await self._repo.get_file(file_id)
        if file is None:
            raise FileNotFound(file_id)

        return file

    async def set_category(self, file_id: FileId, category_id: CategoryId, user_id: UserId) -> File:
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        category = await self._category_getter.get_category(category_id)
        if user_id != category.user_id:
            raise CategoryViolation(category_id, user_id)

        file.category = category
        await self._repo.update_file(file)
        return file

    async def update_title(self, file_id: FileId, title: str, user_id: UserId) -> File:
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        file.title = title
        await self._repo.update_file(file)
        return file

    async def reload_file(self, file_id: FileId, dto: ReloadFileDTO, user_id: UserId) -> File:
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        file.remote_file_id = dto.remote_id
        file.type = dto.file_type
        if dto.title is not None:
            file.title = dto.title

        await self._repo.update_file(file)
        return file

    async def delete_file(self, file_id: FileId, user_id: UserId):
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        await self._repo.delete_file(file_id)

    async def find_files(self,
                         *filters: FilterField,
                         dto: FilesFindDTO = None,
                         paginate: Optional[Pagination] = None,
                         total_count: bool = False) -> tuple[list[File], Optional[int]]:

        dto_items = asdict(dto) if dto else None
        filters = FilterMerger.merge(dto_items, filters)
        FilterMerger.ensure_have_user_id(filters)

        files = await self._repo.find_files(filters, paginate)
        if not total_count:
            return files, None

        files_count = await self._repo.get_files_count(filters)
        return files, files_count
