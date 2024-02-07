from dataclasses import dataclass
from typing import Optional

from app.core.domain.models.category import CategoryId


@dataclass(frozen=True)
class CreateCategoryDTO:
    user_id: int
    title: str
    desc: Optional[str] = None
    marker: Optional[str] = None


@dataclass(frozen=True)
class CategoriesFindDTO:
    user_id: int
    title_match: Optional[str] = None
    favorites: Optional[bool] = None
    have_marker: Optional[bool] = None


@dataclass(frozen=True)
class UpdateCategoryDTO:
    category_id: CategoryId

    title: Optional[str] = None
    desc: Optional[str] = None

    # if delete desc is setup on True
    # and desc is None must set null desc in storage
    delete_desc: Optional[bool] = None
    favorite: Optional[bool] = None

    # convention: If marker is empty string will delete marker.
    marker: Optional[str] = None
