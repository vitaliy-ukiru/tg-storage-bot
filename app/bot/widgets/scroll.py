from typing import Optional, Union

from aiogram_dialog.widgets.common import WhenCondition, Scroll
from aiogram_dialog.widgets.kbd import (
    Row,
    FirstPage,
    CurrentPage,
    NextPage,
    PrevPage, LastPage
)
from aiogram_dialog.widgets.text import Format


class Navigation(Row):
    def __init__(self, scroll_id: Union[str, Scroll], id: Optional[str] = None, when: WhenCondition = None):
        super().__init__(
            FirstPage(scroll=scroll_id, text=Format("<< {target_page1}")),
            PrevPage(scroll=scroll_id),
            CurrentPage(scroll=scroll_id),
            NextPage(scroll=scroll_id),
            LastPage(scroll=scroll_id, text=Format("{target_page1} >>")),
            id=id,
            when=when
        )
