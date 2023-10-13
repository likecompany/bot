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


class InterfaceSettings(BaseSettings):
    INTERFACE_BASE: str


interface_settings = InterfaceSettings()


class FSMSettings(BaseSettings):
    FSM_HOSTNAME: str
    FSM_PORT: int


fsm_settings = FSMSettings()
