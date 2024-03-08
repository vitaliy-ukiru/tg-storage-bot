from .topic import Topic
from .template import Template, TemplateProxy, ParamsGetter, ParamsGetterVariant, I18N_KEY
from .navigation import (BACK_TEXT, CANCEL_TEXT, CLOSE_TEXT,
                         CancelI18n, CloseI18n, BackI18n, BackToI18n)
from .file_title import FileTitle

TL = TemplateProxy()

__all__ = (
    Template,
    Topic,
    TL,
    TemplateProxy,
    BACK_TEXT, CANCEL_TEXT, CLOSE_TEXT,
    CancelI18n, CloseI18n, BackI18n, BackToI18n,
    ParamsGetter, ParamsGetterVariant,
    FileTitle,
    I18N_KEY,
)
