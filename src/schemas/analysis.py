from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    ticker: str
    outlook: str
    key_drivers: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    reasoning: str