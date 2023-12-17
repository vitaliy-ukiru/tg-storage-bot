from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType

from app.core.domain.models.user import UserId

CategoryId = NewType("CategoryId", int)


@dataclass
class Category:
    id: CategoryId
    user_id: UserId
    title: str
    created_at: datetime
    description: Optional[str] = None
    is_favorite: bool = False
