# FinTech Market Intelligence Multi-Agent

A real-time FinTech market intelligence system built using local LLMs and multi-agent orchestration.

## Core Stack

- Ollama
- Qwen3 8B
- LangGraph
- CrewAI
- PydanticAI
- MEM0
- SQLite
- Python
- yfinance
- Financial News
- FinBERT

## Agent Workflow

Researcher → Analyst → Reviewer

## Guardrails

- Maximum execution count: 3
- Conditional routing
- Kill switch
- Safe fallback
- Strict structured output validation

## Memory

MEM0 with SQLite persistence across sessions.

## Objective

Provide evidence-backed market intelligence from real-time/recent market data and financial news while keeping the final investment decision with the human user.

## Status

Phase 1 — Environment setup: COMPLETE

Phase 2 — Python/LangChain/Ollama integration: PENDING