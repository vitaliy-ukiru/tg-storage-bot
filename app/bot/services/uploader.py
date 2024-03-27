from typing import Optional

from aiogram.types import Message

from .file_creds import FileCredentials
from app.core.domain.models.file import File
from app.core.interfaces.usecase import FileUsecase
from app.core.domain.models.auth import Issuer


class FileUploader:
    _uc: FileUsecase

    def __init__(self, uc: FileUsecase):
        self._uc = uc

    async def upload(self,
                     msg: Message,
                     issuer: Issuer,
                     category_id: Optional[int],
                     ) -> File:
        cred = FileCredentials.from_message(msg)
        return await self._uc.save_file(
            cred.to_create_dto(
                issuer.user_id,
                category_id,
            ),
            issuer,
        )
