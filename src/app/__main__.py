import asyncio
import logging

import uvloop

from app.bot import Bot
from app.init import initialize

_LOG = logging.getLogger(__package__)

if __name__ == "__main__":
    config = initialize()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    bot = Bot(config)
    _LOG.info("Running bot")
    bot.run()
