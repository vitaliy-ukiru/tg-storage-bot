from dataclasses import dataclass
from typing import Optional

from aiogram.enums import ContentType
from aiogram.types import Message

from core.domain.file.file_type import FileType
from core.domain.file.dto import ReloadFileDTO


def select_file_name(caption: Optional[str], file_name: Optional[str], file_id: str) -> str:
    if caption is not None:
        return caption

    if file_name is not None:
        return file_name

    return file_id


def file_type_from_mime(mime_type: str) -> FileType:
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
                    title=select_file_name(m.caption, None, photo.file_id)
                )
            case ContentType.DOCUMENT:
                doc = m.document
                return cls(
                    remote_id=doc.file_id,
                    file_type=file_type_from_mime(doc.mime_type),
                    title=select_file_name(m.caption, doc.file_name, doc.file_id)
                )
            case ContentType.AUDIO:
                audio = m.audio
                return cls(
                    remote_id=audio.file_id,
                    file_type=FileType.audio,
                    title=select_file_name(m.caption, audio.file_name, audio.file_id),
                )
            case ContentType.VIDEO:
                video = m.video
                return cls(
                    remote_id=video.file_id,
                    file_type=FileType.video,
                    title=select_file_name(m.caption, video.file_name, video.file_id),
                )
            case ContentType.ANIMATION:
                gif = m.animation
                return cls(
                    remote_id=gif.file_id,
                    file_type=FileType.gif,
                    title=select_file_name(m.caption, gif.file_name, gif.file_id),
                )
            case _:
                raise Exception("invalid media type")


def content_type_from_file(file_type: FileType) -> ContentType:
    match file_type:
        case FileType.photo:
            return ContentType.PHOTO
        case FileType.text, FileType.document:
            return ContentType.DOCUMENT
        case FileType.video:
            return ContentType.VIDEO
        case FileType.audio:
            return ContentType.AUDIO
        case FileType.gif:
            return ContentType.ANIMATION
        case _:
            return ContentType.DOCUMENT
