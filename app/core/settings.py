from __future__ import annotations

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class BotSettings(BaseSettings):
    BOT_TOKEN: str


bot_settings = BotSettings()


class DatabaseSettings(BaseSettings):
    DATABASE_DRIVER: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    BOT_DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    @property
    def url(self) -> str:
        driver, user, password, host, port, name = (
            self.DATABASE_DRIVER,
            self.DATABASE_USERNAME,
            self.DATABASE_PASSWORD,
            self.BOT_DATABASE_HOSTNAME,
            self.DATABASE_PORT,
            self.DATABASE_NAME,
        )

        return f"{driver}://{user}:{password}@{host}:{port}/{name}"


database_settings = DatabaseSettings()


class InterfaceSettings(BaseSettings):
    INTERFACE_BASE: str


interface_settings = InterfaceSettings()


class FSMSettings(BaseSettings):
    FSM_HOSTNAME: str
    FSM_PORT: int


fsm_settings = FSMSettings()
