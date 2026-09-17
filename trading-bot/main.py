from __future__ import annotations

from datetime import datetime, timezone

from src.alpaca_client import get_trading_client
from src.risk_manager import calculate_position_size


DRY_RUN = True


def main() -> None:
    client = get_trading_client()
    account = client.get_account()

    print("AI TRADING BOT — PAPER MODE")
    print(f"Time (UTC): {datetime.now(timezone.utc).isoformat()}")
    print(f"Equity:     {account.equity}")
    print(f"Cash:       {account.cash}")
    print(f"Buying power: {account.buying_power}")
    print()

    # Development sanity check only. No order is submitted here.
    entry = 100.0
    stop = 99.0
    qty = calculate_position_size(
        equity=float(account.equity),
        entry_price=entry,
        stop_price=stop,
        risk_percent=1.0,
        max_notional_percent=10.0,
    )
    print(f"Example risk-sized quantity at ${entry:.2f} with ${stop:.2f} stop: {qty} shares")
    print("DRY RUN: no order submitted.")


if __name__ == "__main__":
    main()
