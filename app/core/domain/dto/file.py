from dataclasses import dataclass
from typing import Optional, Sequence

from app.core.domain.models.file import FileType


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
class FilesFindDTO:
    user_id: int
    category_id: Optional[int] = None
    file_types: Optional[Sequence[FileType]] = None
    title_match: Optional[str] = None
