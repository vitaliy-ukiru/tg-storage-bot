from dataclasses import asdict
from datetime import datetime
from typing import Optional

from app.core.domain.dto.common import Pagination
from app.core.domain.dto.file import CreateFileDTO, ReloadFileDTO, FilesFindDTO
from app.core.domain.exceptions.category import CategoryAccessDenied
from app.core.domain.exceptions.file import FileNotFound, FileAccessDenied
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import File, FileId, RemoteFileId
from app.core.domain.models.user import UserId
from app.core.domain.services.internal import convert_to_filter_fields
from app.core.interfaces.repository.file import (
    FileRepoSaver, FileRepoGetter, FileRepoFinder, FileRepoUpdater, FileRepoDeleter
)
from app.core.interfaces.usecase.category import CategoryGetter
from app.core.interfaces.usecase import FileUsecase

UNDEFINED_FILE_ID = FileId(0)


def _ensure_owner(file: File, user_id: Optional[UserId] = None):
    if user_id is None:
        return

    if file.user_id != user_id:
        raise FileAccessDenied(file.id, user_id)


class FileService(FileUsecase):
    def __init__(
        self,
        saver: FileRepoSaver,
        getter: FileRepoGetter,
        finder: FileRepoFinder,
        updater: FileRepoUpdater,
        deleter: FileRepoDeleter,
        category_getter: CategoryGetter
    ):

        self._saver = saver
        self._getter = getter
        self._finder = finder
        self._updater = updater
        self._deleter = deleter
        self._category_getter = category_getter

    async def save_file(self, dto: CreateFileDTO) -> File:
        file = File(
            UNDEFINED_FILE_ID,
            dto.title,
            dto.file_type,
            RemoteFileId(dto.remote_id),
            dto.remote_unique_id,
            UserId(dto.user_id),
            datetime.now(),
        )

        if dto.category_id is not None:
            category = await self._category_getter.get_category(CategoryId(dto.category_id), file.user_id)
            file.category = category

        file.id = await self._saver.save_file(file)
        return file

    async def get_file(self, file_id: FileId, user_id: Optional[UserId] = None) -> File:
        file = await self._getter.get_file(file_id)
        if file is None:
            raise FileNotFound(file_id)
        _ensure_owner(file, user_id)

        return file

    async def set_category(self, file_id: FileId, category_id: CategoryId, user_id: UserId) -> File:
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        category = await self._category_getter.get_category(category_id, user_id)
        file.category = category
        await self._updater.update_file(file)
        return file

    async def update_title(self, file_id: FileId, title: str, user_id: UserId) -> File:
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        file.title = title
        await self._updater.update_file(file)
        return file

    async def reload_file(self, file_id: FileId, dto: ReloadFileDTO, user_id: UserId) -> File:
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        file.remote_file_id = dto.remote_id
        file.remote_unique_id = dto.remote_unique_id
        file.type = dto.file_type
        if dto.title is not None:
            file.title = dto.title

        await self._updater.update_file(file)
        return file

    async def delete_file(self, file_id: FileId, user_id: UserId):
        file = await self.get_file(file_id, user_id)
        _ensure_owner(file, user_id)

        await self._deleter.delete_file(file_id)

    async def find_files(
        self,
        dto: FilesFindDTO,
        paginate: Optional[Pagination] = None,
        total_count: Optional[bool] = None
    ) -> tuple[list[File], int] | list[File]:
        filters = convert_to_filter_fields(asdict(dto))

        files = await self._finder.find_files(filters, paginate)
        if not total_count:
            return files

        files_count = await self._finder.get_files_count(filters)
        return files, files_count
