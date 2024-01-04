from typing import Optional

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import ManagedMultiselect

from app.bot.handlers.dialogs.file.file_list.common import (
    ID_INPUT_TITLE,
    ID_SELECT_FILE_TYPES,
    CATEGORY_ID_KEY,
    FiltersDict
)
from app.core.domain.dto.file import FilesFindDTO
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import FileType
from app.core.domain.models.user import UserId


class FiltersProxy:
    """
    Is proxy for filters that stores in internal dialog data.
    It gives clear access to all filters, w/o works with manager.

    Also, it gives decorates for set and get values.
    But methods set_file_types and delete_file_types is async
    and because I can't make it as property. It will be ugly.
    """
    manager: DialogManager

    def __init__(self, manager: DialogManager):
        self.manager = manager

    def __get_title_widget(self) -> ManagedTextInput[Optional[str]]:
        return self.manager.find(ID_INPUT_TITLE)

    @property
    def title(self) -> Optional[str]:
        return self.__get_title_widget().get_value()

    @title.setter
    def title(self, value: Optional[str]):
        """
        Setups value for title filter. If value is None it will "delete".
        :param value: Value of filter.  Provide None if you want delete filter.
        """
        managed = self.__get_title_widget()
        managed.widget.set_widget_data(managed.manager, value)

    def __get_file_types_widget(self) -> ManagedMultiselect[FileType]:
        return self.manager.find(ID_SELECT_FILE_TYPES)

    @property
    def file_types(self) -> Optional[list[FileType]]:
        widget = self.__get_file_types_widget()
        items = widget.get_checked()
        if len(items) == 0:
            return None

        return items

    async def set_file_types(self, file_types: Optional[list[FileType]]):
        widget = self.__get_file_types_widget()
        if file_types is None:
            await widget.reset_checked()
            return

        for file_type in file_types:
            await widget.set_checked(file_type, False)

    @property
    def category_id(self) -> Optional[CategoryId | int]:
        category_id = self.manager.dialog_data.get(CATEGORY_ID_KEY)
        return category_id

    @category_id.setter
    def category_id(self, value: Optional[CategoryId | int]):
        """
        Setups or deletes value for category filter.
        If pass None filters will delete.
        :param value: Value of filters. Provide None if you want delete filter.
        :return:
        """
        if value is None:
            del self.manager.dialog_data[CATEGORY_ID_KEY]
            return

        self.manager.dialog_data[CATEGORY_ID_KEY] = value

    def extract_to_dto(self, user_id: UserId) -> FilesFindDTO:
        return FilesFindDTO(
            user_id=user_id,
            category_id=self.category_id,
            title_match=self.title,
            file_types=self.file_types,
        )

    def extract_to_dict(self) -> FiltersDict:
        d = FiltersDict(
            category_id=self.category_id,
            title=self.title,
            file_types=self.file_types,
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
            self.category_id = category_id

        if (file_types := filters.get("file_types")) is not None:
            await self.set_file_types(file_types)
