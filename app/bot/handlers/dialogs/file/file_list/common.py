from typing import Optional, TypedDict

from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import FileType

ID_SELECT_FILE_TYPES = "SELECT_FILE_TYPES"
ID_INPUT_TITLE = "input_title_pattern"
CATEGORY_ID_KEY = "category_id"


class FiltersDict(TypedDict):
    category_id: Optional[CategoryId | int]
    title: Optional[str]
    file_types: Optional[list[FileType]]
