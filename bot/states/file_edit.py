from aiogram.fsm.state import StatesGroup, State


class EditFile(StatesGroup):
    menu_idle = State()
    edit_title = State()
    edit_category = State()
    reload_file = State()
