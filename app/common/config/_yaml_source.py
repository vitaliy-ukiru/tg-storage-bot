__all__ = (
    'YamlSettingsConfigDict',
    'YamlBaseSettings'
)

from pathlib import Path
from typing import Any, Dict, Tuple, ClassVar, Type

import yaml
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pydantic_settings.sources import DotenvType, ENV_FILE_SENTINEL


class YamlSettingsConfigDict(SettingsConfigDict, total=False):
    yaml_file: str | Path | None

class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a YAML file

    Note: slightly adapted version of JsonConfigSettingsSource from docs.
    """

    def __init__(self, settings_class: Type["YamlBaseSettings"]):
        super().__init__(settings_class)
        self._yaml_data = self._load_data(settings_class)

    @staticmethod
    def _load_data(settings: Type["YamlBaseSettings"]) -> Dict[str, Any]:
        """Loads settings from a YAML file at `Config.yaml_file`

        "<file:xxxx>" patterns are replaced with the contents of file xxxx. The root path
        were to find the files is configured with `secrets_dir`.
        """
        yaml_file = settings.model_config.get("yaml_file")

        assert yaml_file, "Settings.yaml_file not properly configured"

        path = Path(yaml_file)

        if not path.exists():
            raise FileNotFoundError(f"Could not open yaml settings file at: {path.absolute()}")

        return yaml.safe_load(path.read_text("utf-8"))

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        field_value = self._yaml_data.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class YamlBaseSettings(BaseSettings):

    # noinspection PyDefaultArgument
    def __init__(self, _case_sensitive: bool | None = None, _env_prefix: str | None = None,
                 _env_file: DotenvType | None = ENV_FILE_SENTINEL, _env_file_encoding: str | None = None,
                 _env_nested_delimiter: str | None = None, _secrets_dir: str | Path | None = None,
                 _yaml_file: str | Path | None = None,
                 **values: Any) -> None:
        if _yaml_file:
            self.model_config["yaml_file"] = _yaml_file

        super().__init__(_case_sensitive, _env_prefix, _env_file, _env_file_encoding,
                         _env_nested_delimiter, _secrets_dir, **values)


    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type["YamlBaseSettings"],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources and their order for
            loading the settings values.
        """
        if not settings_cls.model_config.get("yaml_file"):
            return super().settings_customise_sources(
                settings_cls,
                init_settings,
                env_settings,
                dotenv_settings,
                file_secret_settings
            )

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )

    model_config: ClassVar[YamlSettingsConfigDict] = BaseSettings.model_config


__ALL__ = (YamlBaseSettings,)
