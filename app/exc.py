from __future__ import annotations


class ApplicationError(Exception):
    ...


class CommandUsageError(ApplicationError):
    ...


class InvalidValueError(ApplicationError):
    ...


class GameError(Exception):
    ...


class AdjustError(GameError):
    ...


class NotEnoughBalanceError(GameError):
    ...


class JoinError(GameError):
    ...


class LeftError(GameError):
    ...


class InvalidActionError(GameError):
    ...
