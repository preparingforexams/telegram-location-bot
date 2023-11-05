import logging
import signal
from typing import Any

from telegram import Update
from telegram.ext import Application, CommandHandler

from app.config import Config

_LOG = logging.getLogger(__name__)


class Bot:
    def __init__(self, config: Config):
        self.config = config

    def run(self) -> None:
        app = Application.builder().token(self.config.telegram.token).build()
        app.add_handler(CommandHandler("set_location", self._set_location))
        app.run_polling(
            stop_signals=[signal.SIGTERM],
        )

    async def _set_location(self, update: Update, _: Any) -> None:
        message = update.message

        if message is None:
            _LOG.warning("Stupid sexy filters")
            return

        # TODO: implement
