from typing import Optional

from aiogram.types import Message

from app.bot.utils.files import FileCredentials
from app.core.domain.dto.file import CreateFileDTO
from app.core.domain.models.file import File
from app.core.interfaces.usecase.file import FileUsecase


class FileUploader:
    _uc: FileUsecase

    def __init__(self, uc: FileUsecase):
        self._uc = uc

    async def upload(self, msg: Message, category_id: Optional[int] = None) -> File:
        cred = FileCredentials.from_message(msg)
        return await self._uc.save_file(CreateFileDTO(
            user_id=msg.from_user.id,
            remote_id=cred.remote_id,
            file_type=cred.file_type,
            title=cred.title,
            category_id=category_id
        ))




