from dataclasses import dataclass

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
