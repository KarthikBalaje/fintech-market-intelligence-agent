from pydantic import BaseModel, Field


class ResearchResult(BaseModel):
    ticker: str
    market_summary: str
    news_summary: str
    evidence: list[str] = Field(default_factory=list)