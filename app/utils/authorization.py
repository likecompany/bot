from __future__ import annotations

import hashlib
import hmac
from typing import Optional

from likeinterface.methods import SignIn

from core.settings import bot_settings


def create_telegram_authorization(
    id: int,
    first_name: str,
    last_name: Optional[str],
    username: Optional[str],
    auth_date: int,
) -> SignIn:
    return SignIn(
        telegram_id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        auth_date=auth_date,
        hash=hmac.new(
            hashlib.sha256(bot_settings.BOT_TOKEN.encode()).digest(),
            msg="\n".join(
                [
                    f"{key}={value}"
                    for key, value in sorted(
                        {
                            "id": id,
                            "first_name": first_name,
                            "last_name": last_name,
                            "username": username,
                            "auth_date": auth_date,
                        }.items(),
                        key=lambda x: x[0],
                    )
                ]
            ).encode(),
            digestmod=hashlib.sha256,
        ).hexdigest(),
    )
