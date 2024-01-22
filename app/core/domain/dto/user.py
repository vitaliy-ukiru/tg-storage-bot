from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateUserDTO:
    user_id: int
    locale: Optional[str] = None

@dataclass
class UpdateLocaleDTO:
    user_id: int
    locale: str