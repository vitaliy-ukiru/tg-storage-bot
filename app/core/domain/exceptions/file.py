from app.core.domain.models.file import FileId, RemoteFileId
from .base import DomainException, AccessDenied
from ..models.user import UserId


class FileException(DomainException):
    domain_name = "file"
    file_id: FileId | RemoteFileId

    def __init__(self, file_id: FileId | RemoteFileId, message: str) -> None:
        self.file_id = file_id
        super().__init__(message)

    def _get_message(self):
        message = super()._get_message()
        return f'{message} file_id={self.file_id}'


class StaticFileException(FileException):
    MESSAGE = ""

    def __init__(self, file_id: FileId | RemoteFileId) -> None:
        super(StaticFileException, self).__init__(file_id, self.MESSAGE)

class FileNotFound(StaticFileException):
    MESSAGE = "file not found"


class FileAlreadyExists(StaticFileException):
    MESSAGE = "file with same remote id already exists"

class FileAccessDenied(FileException, AccessDenied):
    user: UserId

    def __init__(self, file_id: FileId | RemoteFileId, user: UserId) -> None:
        self.user = user
        super().__init__(file_id, f"user don't own file {user!r}")

