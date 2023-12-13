from dataclasses import dataclass
from typing import Optional

from aiogram.enums import ContentType
from aiogram.types import Message

from core.domain.models.file import FileType
from core.domain.dto.file import ReloadFileDTO


@dataclass
class FileCredentials:
    remote_id: str
    file_type: FileType
    title: str | None

    def to_reload_dto(self) -> ReloadFileDTO:
        return ReloadFileDTO(self.remote_id, self.file_type, self.title)

    @classmethod
    def from_message(cls, m: Message) -> 'FileCredentials':
        match m.content_type:
            case ContentType.PHOTO:
                photo = m.photo[-1]
                return cls(
                    remote_id=photo.file_id,
                    file_type=FileType.photo,
                    title=m.caption
                )
            case ContentType.DOCUMENT:
                doc = m.document
                return cls(
                    remote_id=doc.file_id,
                    file_type=FileType.document,
                    title=m.caption or doc.file_name
                )
            case ContentType.AUDIO:
                audio = m.audio
                return cls(
                    remote_id=audio.file_id,
                    file_type=FileType.audio,
                    title=m.caption or audio.file_name,
                )
            case ContentType.VIDEO:
                video = m.video
                return cls(
                    remote_id=video.file_id,
                    file_type=FileType.video,
                    title=m.caption or video.file_name,
                )
            case ContentType.ANIMATION:
                gif = m.animation
                return cls(
                    remote_id=gif.file_id,
                    file_type=FileType.gif,
                    title=m.caption or gif.file_name,
                )
            case _:
                raise Exception("invalid media type")


def content_type_from_file(file_type: FileType) -> ContentType:
    match file_type:
        case FileType.photo:
            return ContentType.PHOTO
        case FileType.document:
            return ContentType.DOCUMENT
        case FileType.video:
            return ContentType.VIDEO
        case FileType.audio:
            return ContentType.AUDIO
        case FileType.gif:
            return ContentType.ANIMATION
        case _:
            return ContentType.DOCUMENT
