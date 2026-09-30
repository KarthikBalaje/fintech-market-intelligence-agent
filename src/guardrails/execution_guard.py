def increment_execution(state):
    current = state.get("execution_count", 0)

    return {
        "execution_count": current + 1
    }


def kill_switch(state):
    return {
        "status": "KILLED",
        "final_output": {
            "status": "SAFE_FALLBACK",
            "message": (
                "Analysis stopped because the maximum execution "
                "limit was exceeded. No final investment conclusion "
                "was produced."
            ),
            "execution_count": state.get("execution_count", 0),
        },
    }