from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from bs_nats_updater import NatsConfig

if TYPE_CHECKING:
    from bs_config import Env


@dataclass
class SentryConfig:
    dsn: str
    release: str

    @classmethod
    def from_env(cls, env: Env) -> Self | None:
        dsn = env.get_string("SENTRY_DSN")

        if not dsn:
            return None

        return cls(
            dsn=dsn,
            release=env.get_string("APP_VERSION", default="debug"),
        )


@dataclass
class TelegramConfig:
    token: str
    polling_timeout: int

    @classmethod
    def from_env(cls, env: Env) -> Self:
        token = env.get_string("TELEGRAM_TOKEN")
        if token is None:
            raise ValueError("No Telegram token")

        return cls(
            token=token,
            polling_timeout=env.get_int("TELEGRAM_POLLING_TIMEOUT", default=10),
        )


@dataclass
class Config:
    nats: NatsConfig
    sentry: SentryConfig | None
    telegram: TelegramConfig

    @classmethod
    def from_env(cls, env: Env) -> Self:
        return cls(
            nats=NatsConfig.from_env(env.scoped("NATS_")),
            sentry=SentryConfig.from_env(env),
            telegram=TelegramConfig.from_env(env),
        )
