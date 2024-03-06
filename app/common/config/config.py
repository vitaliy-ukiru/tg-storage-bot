__all__ = (
    'Config',
    'DatabaseConfig',
    'TelegramConfig',
)

from typing import Optional

from pydantic import SecretStr, Field, AliasChoices
from pydantic_settings import BaseSettings

from ._yaml_source import YamlBaseSettings, YamlSettingsConfigDict


class DatabaseConfig(BaseSettings):
    password: Optional[SecretStr] = None
    username: str
    database: str
    host: Optional[str] = None
    port: Optional[int] = None


class TelegramConfig(BaseSettings):
    token: SecretStr
    locales_data_path: str = "data/locales.yaml"


class Config(YamlBaseSettings):
    bot: TelegramConfig
    db: DatabaseConfig = Field(validation_alias=AliasChoices("db", "database"))
    env: str = "local"

    @property
    def is_debug(self) -> bool:
        return self.env != "prod"

    model_config = YamlSettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
    )
