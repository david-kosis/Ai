from __future__ import annotations

from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest

from .alpaca_client import get_trading_client


def submit_paper_market_order(symbol: str, qty: int, side: OrderSide):
    """Submit an order to the Alpaca PAPER environment only."""
    if qty <= 0:
        raise ValueError("qty must be greater than zero")

    client = get_trading_client()
    request = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side,
        time_in_force=TimeInForce.DAY,
    )
    return client.submit_order(order_data=request)
