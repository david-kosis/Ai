from __future__ import annotations


def calculate_position_size(
    equity: float,
    entry_price: float,
    stop_price: float,
    risk_percent: float = 1.0,
    max_notional_percent: float = 10.0,
) -> int:
    """Return whole-share quantity using fixed fractional risk and notional caps."""
    if equity <= 0 or entry_price <= 0 or stop_price <= 0:
        return 0

    risk_per_share = abs(entry_price - stop_price)
    if risk_per_share <= 0:
        return 0

    risk_budget = equity * (risk_percent / 100.0)
    max_notional = equity * (max_notional_percent / 100.0)

    by_risk = int(risk_budget // risk_per_share)
    by_notional = int(max_notional // entry_price)
    return max(0, min(by_risk, by_notional))
