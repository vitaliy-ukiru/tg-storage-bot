from datetime import datetime
from typing import Optional


class User:
    id: int
    created_at: datetime
    deleted_at: Optional[datetime] = None

    def __init__(self, user_id: int, created_at: datetime, deleted_at: Optional[datetime] = None):
        self.id = user_id
        self.created_at = created_at
        self.deleted_at = deleted_at

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def delete(self):
        self.deleted_at = datetime.now()

    def restore(self):
        self.deleted_at = None
