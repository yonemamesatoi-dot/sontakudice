from __future__ import annotations

import os
from pathlib import Path


def load_dotenv_if_present() -> None:
    """最小構成の .env ローダー。"""

    env_path = Path(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_bot_token() -> str:
    load_dotenv_if_present()
    token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "DISCORD_BOT_TOKEN が設定されていません。.env または環境変数を確認してください。"
        )
    return token


def get_guild_id() -> int | None:
    load_dotenv_if_present()
    raw = os.getenv("DISCORD_GUILD_ID", "").strip()
    if not raw:
        return None
    return int(raw)