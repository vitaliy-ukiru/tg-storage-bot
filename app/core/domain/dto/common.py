from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Pagination:
    limit: Optional[int] = None
    offset: Optional[int] = None
