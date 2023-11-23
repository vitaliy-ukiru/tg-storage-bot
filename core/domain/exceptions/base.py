class DomainException(Exception):
    domain_name: str

    def __init__(self, message: str) -> None:
        self.message = message

    def _get_message(self):
        return super().__str__()

    def __str__(self):
        msg = self._get_message()

        return f'domain.{self.domain_name}: {msg}'
