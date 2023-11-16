from core.domain.exceptions import DomainException


class FileException(DomainException):
    domain_name = "file"

    def __init__(self, remote_file_id: str, message: str) -> None:
        self.remote_file_id = remote_file_id
        super().__init__(message)

    def __str__(self):
        message = super(Exception, self).__str__()
        return f'domain.{self.domain_name}: file_id={self.remote_file_id} {message}'


class FileAlreadyExists(FileException):

    def __init__(self, remote_file_id: str) -> None:
        super().__init__(remote_file_id, "file with same remote id already exists")
