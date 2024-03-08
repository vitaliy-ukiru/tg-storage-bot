from typing import Optional

from app.bot.widgets.dao import DialogDataProp, BaseDAO
from app.bot.widgets.dao.widgets import TextInputProp, MultiselectProp

from app.core.domain.dto.file import FilesFindDTO
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import FileCategory
from app.core.domain.models.user import UserId

from .common import (
    ID_INPUT_TITLE,
    ID_SELECT_FILE_TYPES,
    CATEGORY_ID_KEY,
    FiltersDict
)


class FiltersDAO(BaseDAO):
    """
    Is proxy for filters that stores in internal dialog data.
    It gives clear access to all filters, w/o works with manager.

    Also, it gives decorates for set and get values.
    But methods set_file_types and delete_file_types is async
    and because I can't make it as property. It will be ugly.
    """

    title = TextInputProp[Optional[str]](ID_INPUT_TITLE)
    file_types = MultiselectProp[FileCategory](ID_SELECT_FILE_TYPES)
    category = DialogDataProp[CategoryId](CATEGORY_ID_KEY)

    def extract_to_dto(self, user_id: UserId) -> FilesFindDTO:
        return FilesFindDTO(
            user_id=user_id,
            category_id=self.category,
            title_match=self.title,
            file_categories=self.file_types.items,
        )

    def extract_to_dict(self) -> FiltersDict:
        d = FiltersDict(
            category_id=self.category,
            title=self.title,
            file_types=self.file_types.items,
        )
        return {
            k: v
            for k, v in d.items()
            if v is not None
        }

    async def setup(self, filters: FiltersDict):
        """
        Setups only non-empty filters from dict.
        """
        if title := filters.get("title"):
            self.title = title

        if (category_id := filters.get("category_id")) is not None:
            self.category = category_id

        if (file_types := filters.get("file_types")) is not None:
            await self.file_types.setup(file_types)
