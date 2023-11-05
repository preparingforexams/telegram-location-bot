import logging

from app.bot import Bot
from app.init import initialize

_LOG = logging.getLogger(__package__)

if __name__ == "__main__":
    config = initialize()
    bot = Bot(config)
    _LOG.info("Running bot")
    bot.run()
