from core.domain.category import Category
from core.domain.exceptions import DomainException


class FileException(DomainException):
    domain_name = "file"
    file_id: int | str

    def __init__(self, remote_file_id: int | str, message: str) -> None:
        self.file_id = remote_file_id
        super().__init__(message)

    def __str__(self):
        message = super(Exception, self).__str__()
        return f'domain.{self.domain_name}: file_id={self.file_id} {message}'


class FileNotFound(FileException):

    def __init__(self, file_id: int | str) -> None:
        super().__init__(file_id, "file not found")


class FileAlreadyExists(FileException):

    def __init__(self, file_id: int | str) -> None:
        super().__init__(file_id, "file with same remote id already exists")


class FileCategoryViolation(FileException):
    category: str | int | Category

    def __init__(self, file_id: int | str, category: str | int | Category) -> None:
        self.category = category
        super().__init__(file_id, f"user don't own category {category!r}")
