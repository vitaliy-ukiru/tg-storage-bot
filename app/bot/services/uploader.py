from typing import Optional

from aiogram.types import Message

from .file_creds import FileCredentials
from app.core.domain.models.file import File
from app.core.interfaces.usecase import FileUsecase


class FileUploader:
    _uc: FileUsecase

    def __init__(self, uc: FileUsecase):
        self._uc = uc

    async def upload(self, msg: Message, category_id: Optional[int] = None) -> File:
        cred = FileCredentials.from_message(msg)
        return await self._uc.save_file(cred.to_create_dto(msg.from_user.id, category_id))




