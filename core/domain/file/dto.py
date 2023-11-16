from dataclasses import dataclass

from .file_type import FileType


@dataclass(frozen=True)
class CreateFileDTO:
    user_id: int
    remote_id: str
    file_type: FileType
    title: str | None
    category_id: int | None
