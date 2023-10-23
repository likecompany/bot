from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class Settings(BaseModel):
    min_players: int = Field(2, ge=2, le=6)
    max_players: int = Field(6, ge=2, le=6)
    start_time: int = Field(15, gt=0)
    small_blind: int = Field(500, gt=0)
    big_blind_multiplication: int = Field(15, gt=0)
    action_time: int = Field(15, le=40)

    @model_validator(mode="after")
    def check_passwords_match(self) -> Settings:
        if self.min_players > self.max_players:
            raise ValueError("Min players can't be greater than max players")

        return self
