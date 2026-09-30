def analyst_node(state):
    research = state.get("research", {})
    ticker = state.get("ticker", "TMPV")

    market_summary = research.get("market_summary", "")
    news = research.get("news_summary", [])
    
    key_drivers = [
        "Observed market price movement",
    ]

    risks = [
        "Market volatility",
    ]

    if news:
        key_drivers.append(
            "Recent financial news retrieved"
        )
    else:
        risks.append(
            "No financial news evidence available"
        )

    return {
        "analysis": {
            "ticker": ticker,
            "outlook": "NEUTRAL",
            "key_drivers": key_drivers,
            "risks": risks,
            "reasoning": (
                f"Analysis based on retrieved market evidence: "
                f"{market_summary}. "
                f"{len(news)} financial news items were retrieved."
            ),
        }
    }
