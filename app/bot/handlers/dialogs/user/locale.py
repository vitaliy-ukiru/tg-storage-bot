from operator import itemgetter
from typing import Any

from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Radio, ManagedRadio
from aiogram_dialog.widgets.text import Format
from aiogram_i18n import I18nContext

from app.bot.middlewares.user_manager import USER_KEY
from app.bot.states.dialogs import UserChangeLocaleSG
from app.bot.widgets.i18n import TL, CloseI18n
from app.bot.widgets.i18n.template import I18N_KEY

ID_SELECT_LOCALE = "select_lang"

LOCALES = (
    ("🇷🇺 Русский", "ru"),
    ("🇺🇸 English", "en")
)


async def _on_change_locale(_: ChatEvent, __: ManagedRadio, manager: DialogManager, locale: str):
    i18n: I18nContext = manager.middleware_data[I18N_KEY]
    if i18n.locale == locale:
        return

    await i18n.set_locale(locale)


async def _on_start(_: Any, manager: DialogManager):
    i18n: I18nContext = manager.middleware_data[I18N_KEY]
    radio: ManagedRadio = manager.find(ID_SELECT_LOCALE)
    await radio.set_checked(i18n.locale)


user_change_locale = Dialog(
    Window(
        TL.users.locale.select(),
        Radio(
            checked_text=Format("✓ {item[0]}"),
            unchecked_text=Format("{item[0]}"),
            items=LOCALES,
            item_id_getter=itemgetter(1),
            id=ID_SELECT_LOCALE,
            on_state_changed=_on_change_locale
        ),
        CloseI18n(),
        state=UserChangeLocaleSG.main,
    ),
    on_start=_on_start
)
