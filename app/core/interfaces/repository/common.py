from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass(frozen=True)
class FilterField(Generic[T]):
    name: str
    value: T
