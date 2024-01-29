from typing import Container

from app.core.domain.services.user import LocaleValidator


class MemoryLocaleValidator(LocaleValidator):
    def __init__(self, default_locale: str, supported_locales: Container[str]):
        self._default_locale = default_locale
        self._supported_locales = supported_locales

    @property
    def default_locale(self):
        return self._default_locale

    def validate_locale(self, locale: str) -> bool:
        return locale in self._supported_locales
