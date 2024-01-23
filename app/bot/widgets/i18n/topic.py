from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Multi, Text
from .template import Template, TemplateProxy


class Topic(Multi):
    def __init__(self,
                 tmpl: str | TemplateProxy | Template,
                 value: Text,
                 sep: str = ": ",
                 when: WhenCondition = None
                 ):
        if isinstance(tmpl, str):
            tmpl = Template(tmpl)
        elif isinstance(tmpl, TemplateProxy):
            tmpl = tmpl()

        self.tmpl = tmpl
        self.value = value
        self.sep = sep
        super().__init__(tmpl, value, sep=sep, when=when)
