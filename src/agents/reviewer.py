from src.schemas.review import ReviewResult


MIN_NEWS_ARTICLES = 3


def reviewer_node(state):
    research = state.get("research", {})
    execution_count = state.get("execution_count", 0)

    market_status = research.get("data_status")
    news_status = research.get("news_status")
    news = research.get("news_summary", [])
    evidence = research.get("evidence", [])

    missing = []

    if market_status != "REAL_MARKET_DATA":
        missing.append("valid market data")

    if news_status != "REAL_FINANCIAL_NEWS":
        missing.append("financial news source")

    if len(news) < MIN_NEWS_ARTICLES:
        missing.append(
            f"at least {MIN_NEWS_ARTICLES} financial news articles"
        )

    if len(evidence) < 2:
        missing.append("sufficient research evidence")

    # Agent-driven routing decision
    if missing:
        result = ReviewResult(
            decision="NEEDS_MORE_DATA",
            confidence=0.30,
            feedback=(
                "Additional research required: "
                + ", ".join(missing)
            ),
        )

        return {
            "review": result.model_dump(),
            "status": "NEEDS_MORE_DATA",
        }

    result = ReviewResult(
        decision="APPROVED",
        confidence=0.90,
        feedback=(
            f"Evidence threshold satisfied with "
            f"{len(news)} financial news articles "
            f"on execution {execution_count}."
        ),
    )

    return {
        "review": result.model_dump(),
        "status": "APPROVED",
        "final_output": {
            "ticker": state.get("ticker"),
            "status": "APPROVED",
            "message": (
                "Market intelligence analysis completed using "
                "sufficient market and financial-news evidence."
            ),
            "research": research,
            "analysis": state.get("analysis"),
            "review": result.model_dump(),
        },
    }