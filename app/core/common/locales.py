EN = "en"
RU = "ru"

DEFAULT_LOCALE = EN

SUPPORTED_LOCALES = frozenset({EN, RU})


def ensure_locale(locale: str) -> str:
    if locale not in SUPPORTED_LOCALES:
        return DEFAULT_LOCALE

    return locale
