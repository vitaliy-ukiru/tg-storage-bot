from core.domain.exceptions.base import DomainException
from core.domain.models.user import User


class UserException(DomainException):
    domain_name = "user"
    user: User | int

    def __init__(self, user: User | int, message: str) -> None:
        self.user = user
        super().__init__(message)

    def __str__(self):
        message = super().__str__()

        return f'{message}: user={self.user}'


class StaticUserException(UserException):
    MESSAGE = ""

    def __init__(self, user: User | int) -> None:
        super().__init__(user, self.MESSAGE)


class UserAlreadyExists(StaticUserException):
    MESSAGE = "user already exists"


class UserNotFound(StaticUserException):
    MESSAGE = "user not found"


class UserDeleted(StaticUserException):
    MESSAGE = "user deleted"
