from typing import Optional

from aiogram.types import Message

from bot.utils.files import FileCredentials
from core.database import File
from core.domain.file.dto import CreateFileDTO
from core.domain.file.service import FileUseCase


class FileUploader:
    _uc: FileUseCase

    def __init__(self, uc: FileUseCase):
        self._uc = uc

    async def upload(self, msg: Message, category_id: Optional[int] = None) -> File:
        cred = FileCredentials.from_message(msg)
        return await self._uc.create_file(CreateFileDTO(
            user_id=msg.from_user.id,
            remote_id=cred.remote_id,
            file_type=cred.file_type,
            title=cred.title,
            category_id=category_id
        ))




