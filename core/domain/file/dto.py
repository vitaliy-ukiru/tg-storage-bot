from dataclasses import dataclass

from .file_type import FileType


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

    @property
    def non_titled(self) -> bool:
        return self.title is None or self.title == self.remote_id