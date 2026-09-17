from __future__ import annotations

import sys
from pathlib import Path

import yfinance as yf


# Small starter universe for development. The full S&P 500 universe will be added
# after the connection/data pipeline is verified.
STARTER_UNIVERSE = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "TSLA", "AMD", "MU", "NFLX", "GOOGL"]


def gap_percent(symbol: str) -> float | None:
    try:
        data = yf.download(symbol, period="5d", interval="1d", progress=False, auto_adjust=False)
        if len(data) < 2:
            return None
        previous_close = float(data["Close"].iloc[-2].iloc[0] if hasattr(data["Close"].iloc[-2], "iloc") else data["Close"].iloc[-2])
        latest_open = float(data["Open"].iloc[-1].iloc[0] if hasattr(data["Open"].iloc[-1], "iloc") else data["Open"].iloc[-1])
        if previous_close <= 0:
            return None
        return (latest_open / previous_close - 1.0) * 100.0
    except Exception as exc:
        print(f"{symbol}: data error: {exc}", file=sys.stderr)
        return None


def scan(min_gap_percent: float = 3.0) -> list[tuple[str, float]]:
    results: list[tuple[str, float]] = []
    for symbol in STARTER_UNIVERSE:
        gap = gap_percent(symbol)
        if gap is not None and gap >= min_gap_percent:
            results.append((symbol, gap))
    return sorted(results, key=lambda item: item[1], reverse=True)


if __name__ == "__main__":
    print("Starter gap scanner (read-only; no orders are submitted)\n")
    matches = scan()
    if not matches:
        print("No starter-universe gaps >= 3% found in the latest daily data.")
    else:
        for symbol, gap in matches:
            print(f"{symbol}: {gap:.2f}% gap")
