__all__ = (
    'TelegramFile',
    'NamedCategory',
    'File',
)

from datetime import datetime
from typing import Optional

from .file_type import FileType


class TelegramFile:
    file_id: str
    size: Optional[int]
    path: Optional[str]


class NamedCategory:
    id: int
    name: Optional[str]

    def __init__(self, category_id: int, name: Optional[str] = None):
        self.category_id = category_id
        self.name = name

    def __str__(self) -> str:
        if self.name:
            return self.name

        return f'ID[{self.id}]'


DEFAULT_CATEGORY_NAME = "default"


class File:
    id: int
    title: Optional[str]
    type: FileType

    remote_file_id: str
    tg_file: TelegramFile
    user_id: int
    category: Optional[NamedCategory]
    created_at: datetime

    def __init__(self,
                 id_: int,
                 file_type: FileType,
                 remote_file_id: str,
                 user_id: int,
                 created_at: datetime,
                 title: Optional[str] = None,
                 category: Optional[NamedCategory] = None):
        self.id = id_
        self.title = title
        self.type = file_type
        self.remote_file_id = remote_file_id
        self.user_id = user_id
        self.category = category
        self.created_at = created_at

    @property
    def category_name(self) -> str:
        category = self.category
        if category is None:
            return DEFAULT_CATEGORY_NAME

        return str(category)

    @property
    def name(self) -> str:
        return self.title if self.title is not None \
            else self.remote_file_id
