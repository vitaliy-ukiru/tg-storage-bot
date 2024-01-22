from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text, Multi, Const


class Emoji(Multi):
    """
    Emoji is just join widget, it named that for more readability
    """
    def __init__(self, emoji: Text | str, text: Text, sep=" ", when: WhenCondition = None):
        if isinstance(emoji, str):
            emoji = Const(emoji)
        super().__init__(emoji, text, sep=sep, when=when)