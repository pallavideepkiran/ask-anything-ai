# Ask-Anything-AI: Agentic RAG with SQL + Claude 3

A local, intelligent agent that answers natural language questions using your own **PostgreSQL database**. Built with LangChain, Anthropic Claude, and FastAPI.

---
## Architecture

                    ┌────────────────────────────┐
                    │        User Client         │
                    │  (sends natural language)  │
                    └────────────┬───────────────┘
                                 │
                          HTTP POST /ask
                                 │
                    ┌────────────▼────────────┐
                    │      FastAPI App        │
                    │     (app/main.py)       │
                    └────────────┬────────────┘
                                 │
               ┌────────────────▼────────────────┐
               │     LangChain ReAct Agent       │
               │ (SQLDatabase Toolkit + Claude)  │
               └────────────────┬────────────────┘
                                │
                   Generates and executes SQL
                                │
                ┌───────────────▼───────────────┐
                │       PostgreSQL DB           │
                │      ( expenses / dbo)        │
                └───────────────────────────────┘


## How it Works

1. User sends a **natural language query** via `/ask` API.
2. An **LLM-powered agent** translates it into SQL using LangChain's `SQLDatabaseToolkit`.
3. SQL is executed on your **PostgreSQL entitlement database**.
4. The result is returned as **clean JSON** (structured and summarized by Claude).

---

## Tech Stack

- **LangChain**: Agent framework with ReAct
- **Claude 3 (Opus)**: Natural language → SQL & summary
- **SQLAlchemy**: DB interaction
- **FastAPI**: API server
- **PostgreSQL**: Structured data backend

---

## Sample Query

```bash
POST /ask
{
  "question": "List all users with expired licenses grouped by region"
}

