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


class PlayerError(GameError):
    ...


class NotEnoughBalanceError(PlayerError):
    ...


class JoinError(PlayerError):
    ...


class LeftError(PlayerError):
    ...


class ActionError(GameError):
    ...


class NoPossibleActionsError(ActionError):
    ...


class InvalidActionError(ActionError):
    ...
