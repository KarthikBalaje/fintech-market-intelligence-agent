from pathlib import Path

from mem0 import Memory


BASE_DIR = Path(__file__).resolve().parents[2]

MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": str(MEMORY_DIR / "qdrant"),
            "collection_name": "fintech_agent_memory",
            "embedding_model_dims": 768,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "qwen3:8b",
            "temperature": 0,
            "ollama_base_url": "http://localhost:11434",
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": "http://localhost:11434",
        },
    },
    "history_db_path": str(MEMORY_DIR / "mem0_history.db"),
}


memory = Memory.from_config(config)


def save_memory(user_id: str, content: str):
    return memory.add(
        content,
        user_id=user_id,
    )


def search_memory(user_id: str, query: str):
    return memory.search(
        query,
        filters={"user_id": user_id},
    )