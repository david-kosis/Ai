# Quant Gap Breakout Bot

Paper-first, rules-driven S&P 500 gap/breakout trading-bot project.

Pipeline: scan -> rules -> risk -> execute -> manage -> notify -> log -> dashboard

Default broker adapter: Interactive Brokers (IBKR).

IMPORTANT:
- Default mode is paper.
- Live trading requires BOTH BROKER_MODE=live and LIVE_TRADING_ENABLED=true.
- Test extensively in the IBKR paper account before live use.
- This project does not guarantee profitability.

## Install

py -3.12 -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env

Run:
python -m bot.main --mode scan
python -m bot.main --mode trade

Dashboard:
streamlit run dashboard/app.py

Strategy configuration lives in config/rules.json.

Note: "price above today's high" is implemented as a breakout above the previously completed intraday high; a price cannot be above the high of its own still-forming bar.
