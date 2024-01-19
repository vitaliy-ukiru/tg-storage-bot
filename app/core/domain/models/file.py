from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto
from typing import Optional, NewType

from .category import Category
from .user import UserId


class FileCategory(StrEnum):
    unknown = auto()
    photo = auto()
    video = auto()
    document = auto()
    audio = auto()
    gif = auto()


@dataclass
class FileType:
    category: FileCategory
    mime: Optional[str] = None


FileId = NewType("FileId", int)
RemoteFileId = NewType("RemoteFileId", str)


@dataclass
class File:
    id: FileId
    title: Optional[str]
    type: FileType
    remote_file_id: RemoteFileId
    user_id: UserId
    created_at: datetime
    category: Optional[Category] = None

    @property
    def name(self) -> str:
        if self.title:
            return self.title

        return self.remote_file_id[-15:]
