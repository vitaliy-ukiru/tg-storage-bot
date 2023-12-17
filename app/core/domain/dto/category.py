from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateCategoryDTO:
    user_id: int
    title: str
    desc: str | None


@dataclass(frozen=True)
class CategoriesFindDTO:
    user_id: int
    title_match: Optional[str] = None
    favorites: Optional[bool] = None
