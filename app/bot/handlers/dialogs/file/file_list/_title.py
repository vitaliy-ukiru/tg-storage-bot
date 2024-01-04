__all__ = (
    'input_title_window',
)

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const

from app.bot.handlers.dialogs.file.file_list.common import ID_INPUT_TITLE
from app.bot.states.dialogs import FileListSG
from app.bot.utils.optional_str import optional_str_factory
from app.bot.widgets import BackTo, BACK_TEXT


async def _process_input_title(_, __, dialog_manager: DialogManager, ___):
    await dialog_manager.switch_to(FileListSG.main)


input_title_window = Window(
    Const("Введите часть названия файлов"),
    TextInput(
        id=ID_INPUT_TITLE,
        on_success=_process_input_title,
        type_factory=optional_str_factory
    ),
    BackTo(FileListSG.main, BACK_TEXT),
    state=FileListSG.input_file_title,
)
