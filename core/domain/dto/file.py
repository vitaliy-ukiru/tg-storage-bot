from dataclasses import dataclass
from typing import Optional

from core.domain.models.file import FileType


@dataclass(frozen=True)
class CreateFileDTO:
    user_id: int
    remote_id: str
    file_type: FileType
    title: str | None
    category_id: int | None


@dataclass(frozen=True)
class ReloadFileDTO:
    remote_id: str
    file_type: FileType
    title: str | None


@dataclass(frozen=True)
class FilterDTO:
    user_id: int
    category_id: Optional[int] = None
    file_type: Optional[int] = None
    title_match: Optional[str] = None

    def as_tuple(self):
        return (
            ("user_id", self.user_id),
            ("category_id", self.category_id),
            ("file_type", self.file_type),
            ("title_match", self.title_match)
        )