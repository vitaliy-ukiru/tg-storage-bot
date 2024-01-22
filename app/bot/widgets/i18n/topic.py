from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Multi, Text

from app.bot.widgets.i18n import KeyJoiner
from app.bot.widgets.i18n.template import Template


class Topic(Multi):
    def __init__(self,
                 tmpl: str | KeyJoiner | Template,
                 value: Text,
                 sep: str = ": ",
                 when: WhenCondition = None
                 ):
        if not isinstance(tmpl, Template):
            tmpl = Template(tmpl)

        self.tmpl = tmpl
        self.value = value
        self.sep = sep
        super().__init__(tmpl, value, sep=sep, when=when)
