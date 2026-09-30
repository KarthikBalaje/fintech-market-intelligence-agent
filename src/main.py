import sys

from src.graph.workflow import build_graph


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <TICKER>")
        print("Example: python -m src.main TMPV")
        sys.exit(1)

    ticker = sys.argv[1].upper()

    graph = build_graph()

    initial_state = {
        "user_query": (
            f"Analyze {ticker} using available market "
            "and financial information."
        ),
        "ticker": ticker,
        "execution_count": 0,
        "max_executions": 3,
        "status": "STARTED",
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 70)
    print("FINTECH MARKET INTELLIGENCE AGENT")
    print("=" * 70)

    print(f"\nTicker: {ticker}")
    print(f"\nExecution Count: {result.get('execution_count')}")

    print("\nResearch:")
    print(result.get("research"))

    print("\nAnalysis:")
    print(result.get("analysis"))

    print("\nReview:")
    print(result.get("review"))

    print("\nStatus:")
    print(result.get("status"))

    print("\nFinal Output:")
    print(result.get("final_output"))


if __name__ == "__main__":
    main()