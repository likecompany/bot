from typing import List

from aiogram.utils import markdown
from aiogram.utils.link import create_tg_link
from likeinterface import types
from pydantic import ConfigDict, Field

from utils.cards import Card


class Player(types.Player):
    model_config = ConfigDict(frozen=False)

    position: int
    user: types.User
    hand: List[Card] = Field(default_factory=list)

    def url(self) -> str:
        return create_tg_link(link="user", id=self.user.telegram_id)

    def mention_html(self) -> str:
        return markdown.hlink(title=self.user.full_name, url=self.url)
