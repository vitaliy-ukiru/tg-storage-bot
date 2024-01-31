from operator import itemgetter
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Radio, ManagedRadio
from aiogram_dialog.widgets.text import Format
from aiogram_i18n import I18nContext

from app.bot.services.locale import LocaleDisplayer
from app.bot.states.dialogs import UserChangeLocaleSG
from app.bot.widgets.i18n import TL, CloseI18n
from app.bot.widgets.i18n.template import I18N_KEY

ID_SELECT_LOCALE = "select_lang"

LOCALES = (
    ("🇷🇺 Русский", "ru"),
    ("🇺🇸 English", "en")
)

tl = TL.users.locale


async def _on_change_locale(_: ChatEvent, __: ManagedRadio, manager: DialogManager, locale: str):
    i18n: I18nContext = manager.middleware_data[I18N_KEY]
    if i18n.locale == locale:
        return

    await i18n.set_locale(locale)


async def _on_click_close(call: CallbackQuery, __, manager: DialogManager):
    i18n: I18nContext = manager.middleware_data[I18N_KEY]
    if len(manager.current_stack().intents) > 1:
        return

    await call.message.edit_text(i18n.get(str(tl.chosen)))


async def _on_start(_: Any, manager: DialogManager):
    i18n: I18nContext = manager.middleware_data[I18N_KEY]
    radio: ManagedRadio = manager.find(ID_SELECT_LOCALE)
    await radio.set_checked(i18n.locale)

def _locale_getter(data: dict):
    displayer: LocaleDisplayer = data["middleware_data"]["locale_displayer"]
    return [
        (str(locale), locale.code)
        for locale in displayer.get_all_locales()
    ]


user_change_locale = Dialog(
    Window(
        tl.select(),
        Radio(
            checked_text=Format("✓ {item[0]}"),
            unchecked_text=Format("{item[0]}"),
            items=_locale_getter,
            item_id_getter=itemgetter(1),
            id=ID_SELECT_LOCALE,
            on_state_changed=_on_change_locale
        ),
        CloseI18n(
            on_click=_on_click_close
        ),
        state=UserChangeLocaleSG.main,
    ),
    on_start=_on_start
)
