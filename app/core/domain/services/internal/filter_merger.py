from typing import Any, Sequence, Optional, Iterable, Generator

from app.core.domain.exceptions.base import UserNotProvidedError
from app.core.interfaces.repository.common import FilterField


class FilterMerger:
    def __init__(self,
                 data: Optional[dict[str, Any]],
                 native_filters: Iterable[FilterField]):

        self.data = data
        self.native_filters = native_filters

    def _data_filters(self) -> Generator[FilterField]:
        return (
            FilterField(name, value)
            for name, value in self.data.items()
            if value is not None
        )

    def merge(self) -> list[FilterField]:
        filters = {}
        for f in self.native_filters:
            filters[f.name] = f

        if self.data is not None:
            for f in self._data_filters():
                filters[f.name] = f  # override

        if "user_id" not in filters:
            raise UserNotProvidedError()

        return list(filters.values())
