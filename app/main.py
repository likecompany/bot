from __future__ import annotations

import asyncio
import random
import time

from bot import create_bot
from dp import create_dispatcher


async def __main__() -> None:
    dp = create_dispatcher()
    bot = await create_bot()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def main() -> None:
    ttime = int(time.time() * 1000.0)
    random.seed(
        ((ttime & 0xFF000000) >> 24)
        + ((ttime & 0x00FF0000) >> 8)
        + ((ttime & 0x0000FF00) << 8)
        + ((ttime & 0x000000FF) << 24)
    )

    asyncio.run(__main__())


if __name__ == "__main__":
    main()
