from __future__ import annotations

from typing import Callable, Sequence, TypeVar

ArgumentT = TypeVar("ArgumentT")


def count_if(
    collection: Sequence[ArgumentT], condition: Callable[[ArgumentT], bool], weight: int = 1
) -> int:
    return sum(weight for element in collection if condition(element))
