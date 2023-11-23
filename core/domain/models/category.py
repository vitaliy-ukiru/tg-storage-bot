from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType

from core.domain.models.user import UserId

CategoryId = NewType("CategoryId", int)


@dataclass
class Category:
    id: CategoryId
    user_id: UserId
    title: str
    created_at: datetime
    description: Optional[str] = None

    @classmethod
    def from_category_id(cls,
                         category_id: CategoryId,
                         user_id: UserId = 0,
                         title: str = '') -> 'Category':
        return cls(category_id, user_id, title, datetime.now())
