from langgraph.graph import StateGraph, START, END

from src.graph.state import AgentState
from src.agents.researcher import researcher_node
from src.agents.analyst import analyst_node
from src.agents.reviewer import reviewer_node
from src.guardrails.execution_guard import (
    increment_execution,
    kill_switch,
)
from src.graph.routing import route_after_reviewer


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("execution_guard", increment_execution)
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("kill_switch", kill_switch)

    graph.add_edge(START, "execution_guard")
    graph.add_edge("execution_guard", "researcher")

    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        route_after_reviewer,
        {
            "approved": END,
            "research": "execution_guard",
            "kill_switch": "kill_switch",
        },
    )

    graph.add_edge("kill_switch", END)

    return graph.compile()