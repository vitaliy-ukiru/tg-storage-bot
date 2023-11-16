class DomainException(Exception):
    domain_name: str

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self):
        original_message = super().__str__()

        return f'domain.{self.domain_name}: {original_message}'
