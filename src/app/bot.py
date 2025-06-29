import logging
import signal
from typing import Any

from bs_nats_updater import create_updater
from telegram import Update
from telegram.ext import Application, CommandHandler

from app.config import Config

_LOG = logging.getLogger(__name__)


class Bot:
    def __init__(self, config: Config):
        self.config = config

    def run(self) -> None:
        app = (
            Application.builder()
            .updater(
                create_updater(
                    self.config.telegram.token,
                    self.config.nats,
                )
            )
            .build()
        )
        app.add_handler(CommandHandler("set_location", self._set_location))
        app.run_polling(
            stop_signals=[
                signal.SIGINT,
                signal.SIGTERM,
            ],
        )

    async def _set_location(self, update: Update, _: Any) -> None:
        message = update.message

        if message is None:
            _LOG.warning("Stupid sexy filters")
            return

        text = message.text
        if text is None:
            raise ValueError("Message has no text")

        parts = text.split(" ", maxsplit=1)
        if len(parts) == 1 or not (title := parts[1].strip()):
            await message.reply_text(
                "Kein Ort angegeben. Bitte nutze '/set_location Ortsname'.",
            )
            return

        await message.delete()

        user = message.from_user
        if user is None:
            raise ValueError("Message has no from_user")

        chat_id = message.chat_id
        bot = update.get_bot()

        await bot.promote_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            can_invite_users=True,
        )

        await bot.set_chat_administrator_custom_title(
            chat_id=chat_id,
            user_id=user.id,
            custom_title=title,
        )
