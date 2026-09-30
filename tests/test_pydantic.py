import pytest
from pydantic import ValidationError

from src.schemas.research import ResearchResult
from src.schemas.analysis import AnalysisResult
from src.schemas.review import ReviewResult


def test_valid_research_result():
    result = ResearchResult(
        ticker="TMPV",
        market_summary="Market research completed.",
        news_summary="Recent financial news reviewed.",
        evidence=["price data", "news data"],
    )

    assert result.ticker == "TMPV"
    assert len(result.evidence) == 2


def test_valid_analysis_result():
    result = AnalysisResult(
        ticker="TMPV",
        outlook="NEUTRAL",
        key_drivers=["price movement", "news"],
        risks=["volatility"],
        reasoning="Evidence was reviewed.",
    )

    assert result.outlook == "NEUTRAL"


def test_valid_review_result():
    result = ReviewResult(
        decision="APPROVED",
        confidence=0.90,
        feedback="Evidence is sufficient.",
    )

    assert result.decision == "APPROVED"
    assert result.confidence == 0.90


def test_invalid_review_decision():
    with pytest.raises(ValidationError):
        ReviewResult(
            decision="INVALID_DECISION",
            confidence=0.90,
            feedback="Invalid test.",
        )


def test_invalid_confidence():
    with pytest.raises(ValidationError):
        ReviewResult(
            decision="APPROVED",
            confidence=1.5,
            feedback="Invalid confidence.",
        )
