import yfinance as yf


def get_financial_news(ticker: str, limit: int = 5) -> list[dict]:
    symbol = f"{ticker}.NS"

    stock = yf.Ticker(symbol)
    raw_news = stock.news or []

    results = []

    for item in raw_news[:limit]:
        content = item.get("content", {})

        title = content.get("title") or item.get("title")

        if not title:
            continue

        provider = content.get("provider", {})
        publisher = provider.get(
            "displayName",
            "Yahoo Finance",
        )

        results.append(
            {
                "title": title,
                "publisher": publisher,
                "ticker": ticker,
            }
        )

    return results
