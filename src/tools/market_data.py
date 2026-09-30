import math

import yfinance as yf


def get_market_data(ticker: str) -> dict:
    symbol = f"{ticker}.NS"

    stock = yf.Ticker(symbol)

    history = stock.history(
        period="5d",
        interval="1d",
        auto_adjust=False,
    )

    if history.empty:
        raise RuntimeError(f"No market data returned for {symbol}")

    # Remove rows where the actual closing price is unavailable.
    history = history.dropna(subset=["Close"])

    if history.empty:
        raise RuntimeError(
            f"Market data returned for {symbol}, "
            "but no valid closing price was available."
        )

    latest = history.iloc[-1]

    close = float(latest["Close"])
    volume = int(latest["Volume"])

    change_pct = None

    if len(history) >= 2:
        previous_close = float(history.iloc[-2]["Close"])

        if previous_close != 0:
            change_pct = (
                (close - previous_close)
                / previous_close
            ) * 100

    if math.isnan(close):
        raise RuntimeError(
            f"Invalid closing price returned for {symbol}"
        )

    return {
        "ticker": ticker,
        "symbol": symbol,
        "timestamp": str(history.index[-1]),
        "close": close,
        "volume": volume,
        "change_pct": change_pct,
    }
