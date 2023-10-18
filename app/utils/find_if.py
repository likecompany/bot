from __future__ import annotations

from typing import Callable, Optional, Sequence, TypeVar

ArgumentT = TypeVar("ArgumentT")


def find_if(
    collection: Sequence[ArgumentT], condition: Callable[[ArgumentT], bool]
) -> Optional[ArgumentT]:
    for element in collection:
        if condition(element):
            return element

    return None
