from src.alpaca_client import get_trading_client


def main() -> None:
    client = get_trading_client()
    account = client.get_account()
    clock = client.get_clock()

    print("================================")
    print("ALPACA PAPER ACCOUNT CONNECTED")
    print("================================")
    print(f"Account:         {account.account_number}")
    print(f"Status:          {account.status}")
    print(f"Cash:            {account.cash}")
    print(f"Portfolio Value: {account.portfolio_value}")
    print(f"Buying Power:    {account.buying_power}")
    print(f"Market Open:     {clock.is_open}")
    print(f"Next Open:       {clock.next_open}")
    print(f"Next Close:      {clock.next_close}")


if __name__ == "__main__":
    main()
