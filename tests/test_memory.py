from src.memory.mem0_manager import save_memory, search_memory


def test_memory_persistence():
    user_id = "case-study-user"

    save_memory(
        user_id,
        "User prefers NSE market analysis using price movement, "
        "financial news and sentiment.",
    )

    results = search_memory(
        user_id,
        "What type of market analysis does the user prefer?",
    )

    assert results