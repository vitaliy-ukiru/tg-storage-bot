from typing import Any, Callable, Optional

from environs import Env

from . import DbConfig
from .config import Config, TgBot
from .reader import read_config


class Loader:
    def __init__(self, config: dict[str, Any], env: Env):
        self.env = env
        self.config = config

    def load(self) -> Config:
        tg_bot = self.load_tg_bot()
        db = self.load_db_config()
        env = self.config.get('env', 'local')
        return Config(tg_bot, db, env)

    @staticmethod
    def _assert_not_none(val: Any, name: str, type_: type = None, ):
        if val is None:
            raise ValueError(f"{name} must be not None")
        if type_ is not None and not isinstance(val, type_):
            raise ValueError(f'{name} must be {type_!r}')

    def load_tg_bot(self) -> TgBot:
        config = self.config.get('tgbot', {})

        token = config.get('bot_token')
        if (token_env := self.env.str('BOT_TOKEN', None)) is not None:
            token = token_env

        self._assert_not_none(token, 'token', str)
        return TgBot(token)

    def load_db_config(self) -> DbConfig:
        config = self.config.get("database", {})
        env = self.env

        def _get_env(default: Any, key: str, method: Callable = env.str):
            if (v := method(key, None)) is not None:
                return v

            return default

        password = _get_env(config.get('password'), 'DB_PASSWORD')
        username = _get_env(config.get('username'), 'DB_USERNAME')
        database = _get_env(config.get('database'), 'DB_DATABASE')
        host = _get_env(config.get('host'), 'DB_HOST')
        port = _get_env(config.get('port'), 'DB_PORT', env.int)
        if port is not None and not isinstance(port, int):
            raise ValueError("Port must be integer")

        self._assert_not_none(username, 'username', str)
        self._assert_not_none(database, 'database', str)

        return DbConfig(
            password=password,
            username=username,
            database=database,
            host=host,
            port=port,
        )

    @classmethod
    def read(cls, env: Optional[Env] = None, path: Optional[str] = None):
        if env is None:
            env = Env()
            env.read_env()

        if path is None:
            #TODO: doc it env var
            path = env.str("CONFIG_PATH")

        data = read_config(path)
        return cls(data, env)



