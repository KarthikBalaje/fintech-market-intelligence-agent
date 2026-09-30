from datetime import datetime, timezone

from src.tools.market_data import get_market_data
from src.tools.news_search import get_financial_news


def researcher_node(state):
    ticker = state.get("ticker", "TMPV")

    # ---- Market data ----
    try:
        market = get_market_data(ticker)

        market_summary = (
            f"Latest close: {market['close']:.2f}; "
            f"daily change: "
            f"{market['change_pct']:.2f}%"
            if market["change_pct"] is not None
            else f"Latest close: {market['close']:.2f}"
        )

        market_evidence = [
            f"Market timestamp: {market['timestamp']}",
            f"Source: Yahoo Finance via yfinance ({market['symbol']})",
            f"Volume: {market['volume']}",
        ]

        market_status = "REAL_MARKET_DATA"

    except Exception as exc:
        market_summary = f"Market data unavailable: {exc}"
        market_evidence = []
        market_status = "DATA_UNAVAILABLE"

    # ---- Financial news ----
    try:
        news = get_financial_news(ticker, limit=5)

        news_summary = [
            {
                "title": item["title"],
                "publisher": item["publisher"],
            }
            for item in news
        ]

        news_status = "REAL_FINANCIAL_NEWS"

    except Exception:
        news_summary = []
        news_status = "NEWS_UNAVAILABLE"

    evidence = market_evidence

    if news_summary:
        evidence.append(
            f"Financial news articles retrieved: {len(news_summary)}"
        )

    return {
        "research": {
            "ticker": ticker,
            "market_summary": market_summary,
            "news_summary": news_summary,
            "evidence": evidence,
            "data_status": market_status,
            "news_status": news_status,
            "research_timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }
    }
