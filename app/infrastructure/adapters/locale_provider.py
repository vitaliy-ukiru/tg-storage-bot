from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, model_validator, ValidationError

from app.bot.services.locale import LocaleDisplayer, Locale
from app.core.domain.services.user import LocaleValidator


class LocaleProvider(LocaleDisplayer, LocaleValidator):
    def __init__(self, default_locale: str, locales: list[Locale]):
        self._default_locale = default_locale
        self._locales = locales
        self._locales_index = self._build_index()

    @property
    def default_locale(self) -> str:
        return self._default_locale

    def _build_index(self) -> dict[str, Locale]:
        return {
            locale.code: locale
            for locale in self._locales
        }

    def get_locale(self, locale: str) -> Optional[Locale]:
        return self._locales_index.get(locale)

    def get_all_locales(self) -> list[Locale]:
        return self._locales

    def validate_locale(self, locale: str) -> bool:
        return locale in self._locales_index


class LocaleModel(BaseModel):
    code: str
    title: str
    emoji: str


class LocalesResources(BaseModel):
    default_locale: str
    locales: list[LocaleModel]

    @model_validator(mode="after")
    def check_default_locale_contains_in_list(self):
        for locale in self.locales:
            if locale.code == self.default_locale:
                return self
        raise ValidationError("default locales must be contains in locales list")

class ResourcesLocaleProvider(LocaleProvider):
    def __init__(self, res: LocalesResources):
        super().__init__(
            res.default_locale,
            [
                Locale(
                    code=locale.code,
                    title=locale.title,
                    emoji=locale.emoji
                )
                for locale in res.locales
            ])

    @classmethod
    def from_object(cls, obj):
        res = LocalesResources.model_validate(obj)
        return cls(res)


def build_locale_provider(path: str | Path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Could not open yaml locales data file at: {path.absolute()}")

    obj = yaml.safe_load(path.read_text('utf-8'))
    return ResourcesLocaleProvider.from_object(obj)
