def route_after_reviewer(state):
    execution_count = state.get("execution_count", 0)
    review = state.get("review", {})

    max_executions = state.get("max_executions", 3)

    # Kill switch
    if execution_count > max_executions:
        return "kill_switch"

    # Successful review
    if review.get("decision") == "APPROVED":
        return "approved"

    # Continue loop
    return "research"