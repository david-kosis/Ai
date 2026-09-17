from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from alpaca.trading.client import TradingClient


@dataclass(frozen=True)
class Settings:
    api_key: str
    secret_key: str
    paper: bool = True
    live_trading_enabled: bool = False


def load_settings() -> Settings:
    load_dotenv()
    api_key = os.getenv("ALPACA_API_KEY", "").strip()
    secret_key = os.getenv("ALPACA_SECRET_KEY", "").strip()
    paper = os.getenv("ALPACA_PAPER", "true").lower() == "true"
    live_enabled = os.getenv("LIVE_TRADING_ENABLED", "false").lower() == "true"

    if not api_key or not secret_key:
        raise RuntimeError("Missing ALPACA_API_KEY or ALPACA_SECRET_KEY in .env")
    if not paper:
        raise RuntimeError("This research build requires ALPACA_PAPER=true")
    if live_enabled:
        raise RuntimeError("LIVE_TRADING_ENABLED must remain false during development")

    return Settings(api_key, secret_key, paper, live_enabled)


def get_trading_client() -> TradingClient:
    settings = load_settings()
    return TradingClient(settings.api_key, settings.secret_key, paper=True)
