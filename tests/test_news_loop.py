from src.agents.reviewer import reviewer_node


def test_reviewer_requests_more_data_when_news_is_insufficient():
    state = {
        "ticker": "TMPV",
        "execution_count": 1,
        "research": {
            "ticker": "TMPV",
            "market_summary": "Latest close: 280.95",
            "news_summary": [
                {
                    "title": "One financial article",
                    "publisher": "Reuters",
                }
            ],
            "evidence": [
                "Market data retrieved",
                "Financial news retrieved",
            ],
            "data_status": "REAL_MARKET_DATA",
            "news_status": "REAL_FINANCIAL_NEWS",
        },
    }

    result = reviewer_node(state)

    assert result["review"]["decision"] == "NEEDS_MORE_DATA"
    assert "at least 3 financial news articles" in result["review"]["feedback"]
    assert result["status"] == "NEEDS_MORE_DATA"