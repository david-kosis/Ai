# AI Trading Bot — Alpaca Paper Trading

A paper-trading research bot for U.S. equities using Alpaca's official Python SDK (`alpaca-py`).

> **Safety:** This project is configured for Alpaca paper trading only. It does not contain API keys and it defaults to dry-run behavior. Do not put secrets in GitHub.

## Current milestone

- Alpaca paper-account connection test
- Account/clock inspection
- Configurable strategy rules
- Risk-based position sizing
- Market-data scanner scaffold
- Paper-order execution module with an explicit `LIVE_TRADING_ENABLED` safety gate
- Structured trade logging

## Setup on Windows

```powershell
cd trading-bot
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` locally (never commit it):

```env
ALPACA_API_KEY=your_paper_key
ALPACA_SECRET_KEY=your_paper_secret
ALPACA_PAPER=true
LIVE_TRADING_ENABLED=false
```

Run the connection test:

```powershell
python test_connection.py
```

Run the scanner in read-only mode:

```powershell
python -m src.scanner
```

Run the bot in dry-run mode:

```powershell
python main.py
```

## Strategy

The initial rules mirror the tutorial concept but are intentionally treated as a **research specification**, not as a claim of profitability:

- gap >= 3%
- prior close above 200-day SMA
- current price above prior-day high
- price above premarket high when premarket data is available
- relative volume >= 2x when volume history is available
- entry window: 10:05–15:30 America/New_York
- force-close target: 15:51 America/New_York
- maximum risk per trade: 1% of equity
- maximum position notional: 10% of equity
- maximum concurrent positions: 5

The exact implementation and backtest results must be validated before any live use.

## Project structure

```text
trading-bot/
├── .gitignore
├── README.md
├── requirements.txt
├── .env.example
├── rules.json
├── main.py
├── test_connection.py
└── src/
    ├── __init__.py
    ├── alpaca_client.py
    ├── risk_manager.py
    ├── scanner.py
    ├── strategy.py
    └── trader.py
```

## Important

The bot never switches to live trading automatically. `TradingClient(..., paper=True)` is used for the Alpaca connection, and `LIVE_TRADING_ENABLED` must remain `false` during development. Alpaca's official Python SDK is `alpaca-py`. See the official docs before changing execution behavior.
