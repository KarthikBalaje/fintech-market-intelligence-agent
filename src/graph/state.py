from typing import TypedDict


class AgentState(TypedDict, total=False):
    user_query: str
    ticker: str
    research: dict
    analysis: dict
    review: dict
    execution_count: int
    max_executions: int
    status: str
    final_output: dict