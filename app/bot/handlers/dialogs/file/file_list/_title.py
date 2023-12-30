__all__ = (
    'input_title_window',
)

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from app.bot.states.dialogs import FileListSG
from app.bot.widgets import BackTo, BACK_TEXT


async def _process_input_title(_, __, dialog_manager: DialogManager, title_pattern: str):
    filters = dialog_manager.dialog_data.setdefault("filters", {})
    filters["title"] = title_pattern
    await dialog_manager.switch_to(FileListSG.main)


input_title_window = Window(
    Const("Введите часть названия файлов"),
    TextInput(
        id="input_title_pattern",
        on_success=_process_input_title,
    ),
    BackTo(FileListSG.main, BACK_TEXT),
    state=FileListSG.input_file_title,
)
