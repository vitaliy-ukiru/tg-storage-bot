from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass
class Locale:
    code: str
    title: str
    emoji: Optional[str] = None

    def __str__(self):
        if not self.emoji:
            return self.title
        return f'{self.emoji} {self.title}'


class LocaleDisplayer(Protocol):

    @abstractmethod
    def get_locale(self, locale: str) -> Optional[Locale]:
        raise NotImplementedError

    @abstractmethod
    def get_all_locales(self) -> list[Locale]:
        raise NotImplementedError
