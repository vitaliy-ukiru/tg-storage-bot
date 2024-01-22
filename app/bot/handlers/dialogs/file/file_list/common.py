from typing import Optional, TypedDict, Sequence

from app.bot.widgets.i18n import KeyJoiner
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import FileCategory

ID_SELECT_FILE_TYPES = "SELECT_FILE_TYPES"
ID_INPUT_TITLE = "input_title_pattern"
CATEGORY_ID_KEY = "category_id"


class FiltersDict(TypedDict):
    category_id: Optional[CategoryId]
    title: Optional[str]
    file_types: Optional[Sequence[FileCategory]]


lc_file_list = KeyJoiner('file-list')
