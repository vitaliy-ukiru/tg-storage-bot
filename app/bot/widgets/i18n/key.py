from typing import Self


class KeyJoiner:
    __key_separator: str
    __query: tuple[str, ...]

    def __init__(self, *parts: str, key_separator: str = "-", ) -> None:
        self.__key_separator = key_separator
        self.__query = parts

    def __getattr__(self, item: str) -> Self:
        query = self.__query + (item,)
        return KeyJoiner(*query, key_separator=self.__key_separator)

    def __call__(self) -> str:
        return self.__key_separator.join(self.__query)
