from __future__ import annotations


class ApplicationError(Exception):
    ...


class CommandUsageError(ApplicationError):
    ...


class InvalidValueError(ApplicationError):
    ...


class GameError(Exception):
    ...


class CloseGameError(GameError):
    ...


class PlayerError(GameError):
    ...


class JoinError(PlayerError):
    ...


class ExitError(PlayerError):
    ...
