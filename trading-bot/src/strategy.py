from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Candidate:
    symbol: str
    current_price: float
    prior_high: float
    prior_close: float
    sma_200: float
    gap_percent: float
    premarket_high: float | None = None
    relative_volume: float | None = None


def in_entry_window(now: datetime) -> bool:
    eastern = now.astimezone(ZoneInfo("America/New_York"))
    return time(10, 5) <= eastern.time() <= time(15, 30)


def qualifies(candidate: Candidate) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    if candidate.gap_percent < 3.0:
        reasons.append("gap below 3%")
    if candidate.current_price <= candidate.prior_high:
        reasons.append("not above prior-day high")
    if candidate.prior_close <= candidate.sma_200:
        reasons.append("prior close not above 200 SMA")
    if candidate.premarket_high is not None and candidate.current_price <= candidate.premarket_high:
        reasons.append("not above premarket high")
    if candidate.relative_volume is not None and candidate.relative_volume < 2.0:
        reasons.append("relative volume below 2x")

    return not reasons, reasons
