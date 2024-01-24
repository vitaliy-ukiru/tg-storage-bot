__all__ = (
    'input_title_window',
)

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput

from app.bot.handlers.dialogs.file.file_list.common import ID_INPUT_TITLE, tl_file_list
from app.bot.states.dialogs import FileListSG
from app.bot.utils.optional_str import optional_str_factory
from app.bot.widgets.i18n import BackToI18n


async def _process_input_title(_, __, dialog_manager: DialogManager, ___):
    await dialog_manager.switch_to(FileListSG.main)


input_title_window = Window(
    tl_file_list.title.input(),
    TextInput(
        id=ID_INPUT_TITLE,
        on_success=_process_input_title,
        type_factory=optional_str_factory
    ),
    BackToI18n(FileListSG.main),
    state=FileListSG.input_file_title,
)
