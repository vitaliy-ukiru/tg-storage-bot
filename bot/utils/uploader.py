from typing import Optional

from aiogram.enums import ContentType
from aiogram.types import Message

from core.database import File
from core.domain.file import FileType
from core.domain.file.dto import CreateFileDTO
from core.domain.file.service import FileService


class FileUploader:
    _uc: FileService

    def __init__(self, uc: FileService):
        self._uc = uc

    async def upload_by_content_type(self, msg: Message) -> File:
        match msg.content_type:
            case ContentType.PHOTO:
                return await self.upload_photo(msg)
            case ContentType.DOCUMENT:
                return await self.upload_document(msg)
            case ContentType.AUDIO:
                return await self.upload_audio(msg)
            case ContentType.VIDEO:
                return await self.upload_video(msg)
            case ContentType.ANIMATION:
                return await self.upload_gif(msg)

    raise Exception("Invalid content type")

    async def upload_photo(self, msg: Message, category_id: Optional[int] = None) -> File:
        photo = msg.photo[-1]
        return await self._uc.create_file(CreateFileDTO(
            user_id=msg.from_user.id,
            remote_id=photo.file_id,
            file_type=FileType.photo,
            title=select_file_name(msg.caption, None, photo.file_id),
            category_id=category_id
        ))

    async def upload_document(self, msg: Message, category_id: Optional[int] = None):
        doc = msg.document
        file_type = _file_type_from_mime(doc.mime_type)
        return await self._uc.create_file(CreateFileDTO(
            user_id=msg.from_user.id,
            remote_id=doc.file_id,
            file_type=file_type,
            title=select_file_name(msg.caption, doc.file_name, doc.file_id),
            category_id=category_id
        ))

    async def upload_audio(self, msg: Message, category_id: Optional[int] = None):
        audio = msg.audio
        return await self._uc.create_file(CreateFileDTO(
            user_id=msg.from_user.id,
            remote_id=audio.file_id,
            file_type=FileType.audio,
            title=select_file_name(msg.caption, audio.file_name, audio.file_id),
            category_id=category_id
        ))

    async def upload_video(self, msg: Message, category_id: Optional[int] = None):
        video = msg.video
        return await self._uc.create_file(CreateFileDTO(
            user_id=msg.from_user.id,
            remote_id=video.file_id,
            file_type=FileType.video,
            title=select_file_name(msg.caption, video.file_name, video.file_id),
            category_id=category_id
        ))

    async def upload_gif(self, msg: Message, category_id: Optional[int] = None):
        gif = msg.animation
        return await self._uc.create_file(CreateFileDTO(
            user_id=msg.from_user.id,
            remote_id=gif.file_id,
            file_type=FileType.gif,
            title=select_file_name(msg.caption, gif.file_name, gif.file_id),
            category_id=category_id
        ))


def select_file_name(caption: Optional[str], file_name: Optional[str], file_id: str) -> str:
    if caption is not None:
        return caption

    if file_name is not None:
        return file_name

    return file_id


def _file_type_from_mime(mime_type: str) -> FileType:
    mime_base, *_ = mime_type.split('/', 2)
    match mime_base:
        case "image":
            return FileType.photo
        case "video":
            return FileType.video
        case "application":
            return FileType.document
        case "audio":
            return FileType.audio
        case "text":
            return FileType.text
