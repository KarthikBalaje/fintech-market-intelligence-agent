from typing import Literal

from pydantic import BaseModel, Field


class ReviewResult(BaseModel):
    decision: Literal["APPROVED", "NEEDS_MORE_DATA"]
    confidence: float = Field(ge=0.0, le=1.0)
    feedback: str