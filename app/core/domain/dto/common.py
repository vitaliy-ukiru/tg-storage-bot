from dataclasses import dataclass
from enum import StrEnum, unique
from typing import Optional


@dataclass(frozen=True)
class Pagination:
    limit: Optional[int] = None
    offset: Optional[int] = None


@unique
class OrderFields(StrEnum):
    category_id = "category.id"
    category_user = "category.user"
    category_title = "category.title"
    category_description = "category.description"
    category_is_favorite = "category.is_favorite"
    category_created_at = "category.created_at"

    file_id = "file.id"
    file_title = "file.title"
    file_type = "file.type"
    file_user = "file.user"
    file_category = "file.category"
    file_created_at = "file.created_at"


@dataclass
class Ordering:
    field: OrderFields
    reverse: bool = False
