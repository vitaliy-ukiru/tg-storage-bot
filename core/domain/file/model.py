__all__ = (
    'TelegramFile',
    'File',
)

from datetime import datetime
from typing import Optional

from .file_type import FileType
from ..category import Category

DEFAULT_CATEGORY_NAME = "default"


class File:
    id: int
    title: Optional[str]
    type: FileType

    remote_file_id: str
    user_id: int
    category: Optional[Category]
    created_at: datetime

    def __init__(self,
                 file_id: int,
                 file_type: FileType,
                 remote_file_id: str,
                 user_id: int,
                 created_at: datetime,
                 title: Optional[str] = None,
                 category: Optional[Category] = None):
        self.id = file_id
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

        return category.title

    @property
    def name(self) -> str:
        return self.title if self.title is not None else self.remote_file_id
