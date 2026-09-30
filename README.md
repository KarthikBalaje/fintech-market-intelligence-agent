# Case Study 2 — FinTech Market Intelligence Multi-Agent

A guarded multi-agent FinTech market-intelligence system built using **LangGraph, Pydantic, PydanticAI, CrewAI, Ollama/Qwen3, yfinance, and MEM0**.

The system retrieves market data and financial news for a user-supplied stock ticker, analyzes the collected evidence, and uses a Reviewer agent to determine whether sufficient evidence exists.

> **Important:** This system is designed for human decision support. It does not execute trades or make autonomous investment decisions.

---

## 1. Case Study Objective

The objective of this case study is to demonstrate a production-oriented agentic workflow with:

- Multi-agent orchestration
- Conditional agent-to-agent routing
- Evidence-driven looping
- Execution-budget guardrails
- Kill switch and safe fallback
- Structured output validation
- Persistent memory
- Local LLM integration
- Real-time market data
- Financial-news retrieval
- Automated testing
- PydanticAI structured-output demonstration
- CrewAI multi-agent demonstration

The **primary orchestration framework is LangGraph**.

---

## 2. Evaluation Mapping

| Evaluation Area | Implementation | Status |
|---|---|---|
| Agent graph structure | LangGraph: Researcher → Analyst → Reviewer | PASS |
| Loop / execution guardrail | `execution_count` with maximum execution limit | PASS |
| Kill switch / fallback | Dedicated `kill_switch` node | PASS |
| Structured output validation | Pydantic models | PASS |
| Persistent memory | MEM0 with local persistence | PASS |
| Design documentation | Architecture and design documentation | PASS |
| Local LLM | Ollama + Qwen3 8B configured/tested | PASS |
| Real market data | yfinance | PASS |
| Financial news | Yahoo Finance through yfinance | PASS |
| PydanticAI | Isolated structured-output demonstration | PASS |
| CrewAI | Isolated Researcher → Analyst → Reviewer demonstration | PASS |

### Framework clarification

LangGraph is the **primary workflow framework**.

PydanticAI and CrewAI are included as isolated framework demonstrations. They do not replace the primary LangGraph workflow.

---

## 3. High-Level Architecture

```text
                         User
                          |
                          | Ticker
                          v
                    +-------------+
                    |  main.py    |
                    +-------------+
                          |
                          v
                  +---------------+
                  |   LangGraph   |
                  +---------------+
                          |
                          v
                 +------------------+
                 |    Researcher    |
                 +------------------+
                    |            |
                    v            v
              Market Data    Financial News
                 yfinance       yfinance
                    \            /
                     \          /
                      v        v
                 +------------------+
                 |     Analyst      |
                 +------------------+
                          |
                          v
                 +------------------+
                 |     Reviewer     |
                 +------------------+
                          |
                 Is evidence sufficient?
                     /           \
                   YES            NO
                    |              |
                    v              v
               APPROVED       NEEDS_MORE_DATA
                    |              |
                    v              |
                   END <-----------+
                                   |
                              Research again
                                   |
                            Execution Guard
                                   |
                        execution_count > 3
                                   |
                                   v
                           +---------------+
                           |  Kill Switch  |
                           +---------------+
                                   |
                                   v
                            SAFE_FALLBACK
```

---

## 4. Agent Responsibilities

### 4.1 Researcher

The Researcher collects external evidence.

It retrieves:

- Latest market price
- Daily price movement
- Trading volume
- Market timestamp
- Recent financial-news articles
- Publisher information

Primary data source:

```text
yfinance
```

The ticker is supplied by `main.py` and passed through LangGraph state.

Example:

```powershell
python -m src.main TMPV
```

### 4.2 Analyst

The Analyst consumes the Researcher output and creates structured market intelligence.

It produces:

- Outlook
- Key drivers
- Risks
- Reasoning

The current evaluated implementation uses deterministic analysis logic for reproducibility and execution speed.

### 4.3 Reviewer

The Reviewer is the workflow decision gate.

It evaluates:

- Market-data availability
- Financial-news availability
- Number of financial-news articles
- Research evidence

The current minimum financial-news threshold is:

```text
3 articles
```

Therefore:

```text
News >= 3
    ↓
APPROVED
```

and:

```text
News < 3
    ↓
NEEDS_MORE_DATA
```

The Reviewer makes the routing decision. There is no human-controlled `force_review_loop` in the production flow.

---

## 5. Agentic Loop

### Normal flow

```text
Researcher
    ↓
Analyst
    ↓
Reviewer
    ↓
Evidence sufficient
    ↓
APPROVED
    ↓
END
```

### Insufficient-evidence flow

```text
Researcher
    ↓
Analyst
    ↓
Reviewer
    ↓
NEEDS_MORE_DATA
    ↓
Researcher
    ↓
Analyst
    ↓
Reviewer
```

The graph continues until:

1. The Reviewer approves the evidence, or
2. The execution limit is exceeded.

---

## 6. Execution Guardrail

The LangGraph state contains:

```python
execution_count
max_executions
```

The default maximum is:

```python
max_executions = 3
```

The execution guard increments the counter before each research cycle.

Routing behavior:

```text
execution_count <= 3
        |
        +---- Continue workflow

execution_count > 3
        |
        +---- Kill Switch
```

This prevents an unbounded agentic loop.

---

## 7. Kill Switch and Safe Fallback

The kill switch is implemented as a dedicated LangGraph node.

When the execution budget is exceeded:

```text
KILL SWITCH
     |
     v
SAFE_FALLBACK
```

The system intentionally does not produce a final investment conclusion.

Example:

```text
Analysis stopped because the maximum execution
limit was exceeded. No final investment conclusion
was produced.
```

This provides a deterministic safety boundary.

---

## 8. Structured Output Validation

The project uses Pydantic models for structured validation.

### ResearchResult

```python
class ResearchResult(BaseModel):
    ticker: str
    market_summary: str
    news_summary: str
    evidence: list[str]
```

### AnalysisResult

```python
class AnalysisResult(BaseModel):
    ticker: str
    outlook: str
    key_drivers: list[str]
    risks: list[str]
    reasoning: str
```

### ReviewResult

```python
class ReviewResult(BaseModel):
    decision: Literal["APPROVED", "NEEDS_MORE_DATA"]
    confidence: float
    feedback: str
```

The Review schema restricts the decision to:

```text
APPROVED
NEEDS_MORE_DATA
```

and validates confidence between:

```text
0.0 and 1.0
```

---

## 9. PydanticAI Demonstration

PydanticAI is included as a separate structured-output demonstration.

The demonstration uses a typed output model:

```text
MarketReview
    |
    +-- decision
    +-- confidence
    +-- feedback
```

Run:

```powershell
python -m src.frameworks.pydantic_ai_demo
```

Example:

```text
PydanticAI structured output:
decision='APPROVED' confidence=0.0 feedback='a'
```

This demonstrates that PydanticAI can produce output conforming to the declared schema.

The demonstration is intentionally isolated from the primary LangGraph workflow.

---

## 10. CrewAI Demonstration

CrewAI is included as a minimal multi-agent framework demonstration.

The demonstration contains:

```text
Researcher
    ↓
Analyst
    ↓
Reviewer
```

with a sequential process.

Run:

```powershell
python -m src.frameworks.crewai_demo
```

Expected:

```text
CrewAI demonstration configured successfully.
Agents: Researcher -> Analyst -> Reviewer
Process: sequential
```

CrewAI is intentionally not used as the primary orchestration framework.

---

## 11. Local LLM — Ollama / Qwen3

The project is configured for local LLM execution through Ollama.

Configured model:

```text
qwen3:8b
```

The LangChain integration is implemented in:

```text
src/llm/model.py
```

Example:

```python
from langchain_ollama import ChatOllama

def get_llm():
    return ChatOllama(
        model="qwen3:8b",
        temperature=0.2,
    )
```

### Important implementation note

The Ollama/Qwen3 integration is configured and tested separately.

The current evaluated Researcher, Analyst, and Reviewer graph nodes use deterministic logic for reproducibility and speed.

Therefore, the current implementation should **not be described as a fully LLM-generated agent graph**.

---

## 12. Persistent Memory — MEM0

MEM0 is used for persistent memory across sessions.

Memory implementation:

```text
src/memory/mem0_manager.py
```

Local persistent memory is stored under:

```text
memory/
```

The memory test verifies that information written during one operation can be retrieved later.

Run:

```powershell
pytest -q tests\test_memory.py
```

---

## 13. Market Data

Market data is retrieved using:

```text
yfinance
```

NSE symbols are constructed by appending:

```text
.NS
```

For example:

```text
TMPV
```

becomes:

```text
TMPV.NS
```

The system retrieves:

- Closing price
- Daily percentage change
- Volume
- Market timestamp

Successful demonstration:

```text
Ticker: TMPV
Execution Count: 1

data_status: REAL_MARKET_DATA
news_status: REAL_FINANCIAL_NEWS

Financial news articles retrieved: 5

Review:
decision='APPROVED'
confidence=0.9

Status:
APPROVED
```

---

## 14. Ticker Consideration

The original demonstration used:

```text
TATAMOTORS
```

Yahoo Finance returned no market data for:

```text
TATAMOTORS.NS
```

The project therefore uses:

```text
TMPV
```

for the successful market-data demonstration.

The TATAMOTORS scenario is also useful for demonstrating the system's behavior when required market data is unavailable.

---

## 15. Project Structure

```text
fintech-market-intelligence-agent/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── model.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── workflow.py
│   │   └── routing.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── researcher.py
│   │   ├── analyst.py
│   │   └── reviewer.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── market_data.py
│   │   ├── news_search.py
│   │   └── sentiment.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── research.py
│   │   ├── analysis.py
│   │   └── review.py
│   │
│   ├── guardrails/
│   │   ├── __init__.py
│   │   └── execution_guard.py
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   └── mem0_manager.py
│   │
│   └── frameworks/
│       ├── __init__.py
│       ├── pydantic_ai_demo.py
│       └── crewai_demo.py
│
├── tests/
│   ├── __init__.py
│   ├── test_llm.py
│   ├── test_tools.py
│   ├── test_graph.py
│   ├── test_guardrail.py
│   ├── test_pydantic.py
│   ├── test_memory.py
│   └── test_news_loop.py
│
├── memory/
│   └── .gitkeep
│
├── evidence/
│   ├── 01_environment/
│   ├── 02_agent_graph/
│   ├── 03_realtime_data/
│   ├── 04_guardrail/
│   ├── 05_kill_switch/
│   ├── 06_pydantic/
│   ├── 07_memory/
│   └── 08_final_demo/
│
└── docs/
    ├── architecture.md
    ├── design-decisions.md
    └── evaluation-matrix.md
```

---

## 16. Prerequisites

Recommended environment:

- Windows 10/11
- Python 3.10
- Git
- PowerShell
- Ollama

Verify Python:

```powershell
python --version
```

Verify Git:

```powershell
git --version
```

Verify Ollama:

```powershell
ollama --version
```

Verify installed models:

```powershell
ollama list
```

Required model:

```text
qwen3:8b
```

Install if necessary:

```powershell
ollama pull qwen3:8b
```

MEM0 embedding model:

```powershell
ollama pull nomic-embed-text
```

---

## 17. Environment Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create environment file:

```powershell
Copy-Item .env.example .env
```

Review `.env` before running the application.

---

## 18. Run the Application

The ticker is passed from the command line.

### TMPV

```powershell
python -m src.main TMPV
```

### SBIN

```powershell
python -m src.main SBIN
```

### Any other supported NSE ticker

```powershell
python -m src.main <TICKER>
```

The ticker is not hard-coded in the primary execution path.

---

## 19. Successful Scenario

Run:

```powershell
python -m src.main TMPV
```

Expected behavior:

```text
Ticker: TMPV
Execution Count: 1

REAL_MARKET_DATA
REAL_FINANCIAL_NEWS
5 financial news articles

Reviewer:
APPROVED

Status:
APPROVED
```

This demonstrates:

```text
Researcher
    ↓
Analyst
    ↓
Reviewer
    ↓
APPROVED
    ↓
END
```

---

## 20. Guardrail Scenario

Run:

```powershell
python -m src.main TATAMOTORS
```

When required market data is unavailable, the Reviewer can return:

```text
NEEDS_MORE_DATA
```

The workflow loops.

When the execution budget is exceeded:

```text
Execution Count: 4
Status: KILLED
```

Final output:

```text
status: SAFE_FALLBACK
```

The system therefore demonstrates:

```text
Missing evidence
      ↓
NEEDS_MORE_DATA
      ↓
Research loop
      ↓
Execution limit
      ↓
KILL SWITCH
      ↓
SAFE_FALLBACK
```

---

## 21. Testing

Run the complete suite:

```powershell
pytest -q
```

Final validation result:

```text
8 passed
```

Individual tests:

```powershell
pytest -q tests\test_graph.py
```

```powershell
pytest -q tests\test_guardrail.py
```

```powershell
pytest -q tests\test_news_loop.py
```

```powershell
pytest -q tests\test_pydantic.py
```

```powershell
pytest -q tests\test_memory.py
```

---

## 22. Evidence Capture

The project contains an evidence directory for evaluation.

### Successful path

```powershell
python -m src.main TMPV |
    Tee-Object .\evidence\08_final_demo\positive_path.txt
```

### Kill-switch path

```powershell
python -m src.main TATAMOTORS |
    Tee-Object .\evidence\05_kill_switch\kill_switch_demo.txt
```

### News sufficiency test

```powershell
pytest -q tests\test_news_loop.py |
    Tee-Object .\evidence\04_guardrail\news_sufficiency_test.txt
```

### Kill-switch test

```powershell
pytest -q tests\test_guardrail.py |
    Tee-Object .\evidence\05_kill_switch\kill_switch_test.txt
```

### PydanticAI

```powershell
python -m src.frameworks.pydantic_ai_demo |
    Tee-Object .\evidence\06_pydantic\pydantic_ai_demo.txt
```

### CrewAI

```powershell
python -m src.frameworks.crewai_demo |
    Tee-Object .\evidence\08_final_demo\crewai_demo.txt
```

### Full test suite

```powershell
pytest -q |
    Tee-Object .\evidence\08_final_demo\all_tests.txt
```

---

## 23. Final Implementation Summary

```text
                    FINTECH MARKET
                  INTELLIGENCE AGENT
                          |
                          v
                     LangGraph
                          |
              +-----------+-----------+
              |           |           |
              v           v           v
         Researcher    Analyst     Reviewer
              |                       |
              |                       |
        Market + News          Evidence Gate
                                      |
                            +---------+---------+
                            |                   |
                            v                   v
                        APPROVED          NEEDS_MORE_DATA
                            |                   |
                            v                   v
                           END             Researcher
                                               |
                                               v
                                         Execution Guard
                                               |
                                        count > 3 ?
                                               |
                                               v
                                          Kill Switch
                                               |
                                               v
                                         SAFE_FALLBACK
```

The final implementation demonstrates a **bounded, evidence-driven multi-agent FinTech workflow** with conditional routing, structured validation, persistent memory, real market/news retrieval, execution guardrails, and safe termination behavior.
