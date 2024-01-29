class DomainException(Exception):
    domain_name: str

    def __init__(self, message: str) -> None:
        self.message = message

    def _get_message(self):
        return super().__str__()

    def __str__(self):
        msg = self._get_message()

        return f'domain.{self.domain_name}: {msg}'


class InvalidFilterError(DomainException):
    filter_name: str
    domain_name = "core"

    def __init__(self, filter_name: str) -> None:
        self.filter_name = filter_name
        super().__init__(f"unknown filter {filter_name!r} ")


class UserNotProvidedError(DomainException):
    domain_name = "core"

    def __init__(self):
        super().__init__(f'user not provided')


class AccessDenied(DomainException):
    pass
