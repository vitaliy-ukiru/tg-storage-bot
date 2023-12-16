from dataclasses import dataclass
from typing import Any, Optional, Callable

from environs import Env


@dataclass
class DbConfig:
    password: Optional[str]
    username: str
    database: str
    host: Optional[str]
    port: Optional[int]
@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    env: str

    @property
    def is_debug(self) -> bool:
        return self.env != "prod"







