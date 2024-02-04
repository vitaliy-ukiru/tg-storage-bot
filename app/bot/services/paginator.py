import math

from app.core.domain.dto.common import Pagination


class Paginator:
    per_page: int
    current_page: int

    def __init__(self, per_page: int, current_page: int):
        self.per_page = per_page
        self.current_page = current_page

    @property
    def pagination(self) -> Pagination:
        return Pagination(
            self.per_page,
            self.current_page * self.per_page,
        )

    def get_page_count(self, total: int) -> int:
        return math.ceil(total / self.per_page)
