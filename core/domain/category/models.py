from datetime import datetime


class Category:
    id: int
    user_id: int

    title: str
    description: str | None
    created_at: datetime
