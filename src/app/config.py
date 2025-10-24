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
        dsn = env.get_string("sentry-dsn")

        if not dsn:
            return None

        return cls(
            dsn=dsn,
            release=env.get_string("app-version", default="debug"),
        )


@dataclass
class TelegramConfig:
    token: str
    polling_timeout: int

    @classmethod
    def from_env(cls, env: Env) -> Self:
        return cls(
            token=env.get_string("token", required=True),
            polling_timeout=env.get_int("polling-timeout", default=10),
        )


@dataclass
class Config:
    nats: NatsConfig
    sentry: SentryConfig | None
    telegram: TelegramConfig

    @classmethod
    def from_env(cls, env: Env) -> Self:
        return cls(
            nats=NatsConfig.from_env(env / "nats"),
            sentry=SentryConfig.from_env(env),
            telegram=TelegramConfig.from_env(env / "telegram"),
        )
