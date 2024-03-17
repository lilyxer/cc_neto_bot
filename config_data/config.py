from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str
    db_port: str

    def DSN(self) -> str:
        return (f'postgresql+asyncpg://{self.db_user}:{self.db_password}@'
                f'{self.db_host}:{self.db_port}/{self.database}')


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str|None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('bot_token')),
        db=DatabaseConfig(database=env('db_name'),
                               db_host=env('db_localhost'),
                               db_user=env('db_login'),
                               db_password=env('db_password'),
                               db_port=env('db_port'))
        )

_CONFIG = load_config()


if __name__ == '__main__':
    conf = load_config()
    print(conf.db.DSN())