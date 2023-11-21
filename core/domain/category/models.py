from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Category:
    id: int
    user_id: int
    title: str
    created_at: datetime
    description: Optional[str] = None
