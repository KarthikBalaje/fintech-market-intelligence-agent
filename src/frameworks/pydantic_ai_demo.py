from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent


class MarketReview(BaseModel):
    decision: Literal["APPROVED", "NEEDS_MORE_DATA"]
    confidence: float = Field(ge=0.0, le=1.0)
    feedback: str


def build_pydantic_ai_agent():
    return Agent(
        "test",
        output_type=MarketReview,
        instructions=(
            "Return a structured market review. "
            "Use APPROVED when sufficient evidence exists. "
            "Use NEEDS_MORE_DATA otherwise."
        ),
    )


def run_demo():
    agent = build_pydantic_ai_agent()

    result = agent.run_sync(
        "There are 5 financial news articles and valid market data."
    )

    print("PydanticAI structured output:")
    print(result.output)


if __name__ == "__main__":
    run_demo()