from typing import Any, Sequence, Optional

from app.core.domain.exceptions.base import UserNotProvidedError
from app.core.interfaces.repository.common import FilterField


class FilterMerger:
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> list[FilterField]:
        return [
            FilterField(name, value)
            for name, value in data.items()
            if value is not None
        ]

    @classmethod
    def merge_filters(cls, data: Optional[dict[str, Any]], native_filters: Sequence[FilterField]):
        filters = {}
        for f in native_filters:
            filters[f.name] = f

        if data is not None:
            for f in cls.from_dict(data):
                filters[f.name] = f  # override

        return list(filters.values())

    @classmethod
    def ensure_have_user_id(cls, filters: Sequence[FilterField]):
        for f in filters:
            if f.name == "user_id":
                break
        else:
            raise UserNotProvidedError()
