from app.core.domain.exceptions.base import UserNotProvidedError
from app.core.interfaces.repository.common import FilterField


def convert_to_filter_fields(data: dict) -> list[FilterField]:
    if not data.get("user_id"):
        raise UserNotProvidedError()

    return [
        FilterField(name, value)
        for name, value in data.items()
        if value is not None
    ]
