from pydantic import BaseModel

from enums import Rank, Suit


class Card(BaseModel):
    rank: Rank
    suit: Suit

    def as_string_pretty(self) -> None:
        return self.rank.to_string_pretty() + self.suit.to_string_pretty()

    def __str__(self) -> str:
        return self.rank.value + self.suit.value
