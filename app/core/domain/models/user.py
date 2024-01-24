from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType

UserId = NewType("UserId", int)

@dataclass
class User:
    id: UserId
    locale: str
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def delete(self):
        self.deleted_at = datetime.now()

    def restore(self):
        self.deleted_at = None
