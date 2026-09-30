from src.graph.workflow import build_graph


def test_kill_switch(monkeypatch):
    def insufficient_news_researcher(state):
        return {
            "research": {
                "ticker": state["ticker"],
                "market_summary": "Latest close: 280.95",
                "news_summary": [
                    {
                        "title": "Only one article",
                        "publisher": "Test Source",
                    }
                ],
                "evidence": [
                    "Market data retrieved",
                    "Financial news retrieved",
                ],
                "data_status": "REAL_MARKET_DATA",
                "news_status": "REAL_FINANCIAL_NEWS",
            }
        }

    monkeypatch.setattr(
        "src.graph.workflow.researcher_node",
        insufficient_news_researcher,
    )

    graph = build_graph()

    state = {
        "user_query": "Guardrail test",
        "ticker": "TMPV",
        "execution_count": 0,
        "max_executions": 3,
        "status": "STARTED",
    }

    result = graph.invoke(state)

    assert result["execution_count"] > 3
    assert result["status"] == "KILLED"
    assert result["final_output"]["status"] == "SAFE_FALLBACK"