from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


def _parse_int_env(name: str) -> int | None:
    raw = os.getenv(name, "").strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_id: int | None
    channel_url: str | None
    channel_id: int | None


def load_settings() -> Settings:
    cwd = Path.cwd()
    env_path = cwd / ".env"
    env_example_path = cwd / ".env.example"

    if env_path.exists():
        load_dotenv(env_path, override=False)
    elif env_example_path.exists():
        load_dotenv(env_example_path, override=False)

    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError(
            "BOT_TOKEN is missing. Put it in .env or .env.example, or set it in environment."
        )

    admin_id = _parse_int_env("ADMIN_ID")

    raw_channel_url = os.getenv("CHANNEL_URL", "").strip()
    channel_url = raw_channel_url if raw_channel_url else None

    channel_id = _parse_int_env("CHANNEL_ID")

    return Settings(bot_token=token, admin_id=admin_id, channel_url=channel_url, channel_id=channel_id)
