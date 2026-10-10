# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Multi-agent "supervisor" system built with LangChain 1.x (`langchain.agents.create_agent`) and Groq chat models (`langchain_groq.ChatGroq`, e.g. `llama-3.3-70b-versatile`). A supervisor agent receives the user's question and delegates it to specialist agents. Code, prompts, identifiers and user-facing output are in Spanish — keep that convention.

## Environment & commands

- Python >= 3.14, virtualenv at `./venv` (basedpyright is configured to use it via `[tool.basedpyright]` in `pyproject.toml`).
- Install: `source venv/bin/activate && pip install -e .` (or `pip install -r requirements.txt`, which pins exact versions). Note `[tool.setuptools] py-modules = ["agent"]` points at a module that doesn't exist.
- `.env` at the repo root must define `GROQ_API_KEY`; optional `LANGSMITH_*` vars enable tracing. Entry code calls `load_dotenv()`.
- Modules import each other as top-level siblings (`from agente_clima import AgenteClima`), so run scripts from inside `agente_supervisor/` (e.g. `cd agente_supervisor && python supervisor.py`).
- There are no tests, linter config, or build steps.

## Architecture

All code is in `agente_supervisor/`:

- **Specialist agents** (`agente_clima.py` → `AgenteClima`, `agente_calendario.py` → `AgenteCalendario`) share one pattern: the constructor takes a chat model and builds a `create_agent(...)` with a Spanish system prompt and tools; `procesar(input)` invokes it with a single user message (`recursion_limit: 6`) and returns the last message's content. Tools are `@tool`-decorated functions defined as class attributes **without `self`** and passed as `self.<tool_name>`. Tools currently return hard-coded sample data (Monterrey, Guadalajara, Ciudad de México).
- **Supervisor** (`supervisor.py` → `Supervisor(model, agente_clima, agente_calendario)`): wraps each specialist's `procesar` in a closure `@tool` (`delegar_a_agente_clima`, `delegar_a_agente_calendario`) whose docstring drives routing, builds its own `create_agent` over those tools, and runs a REPL in `chat()` (`recursion_limit: 8`, exits on `salir`/`exit`). It may call multiple specialists for mixed requests.
- Adding a specialist = new class following the same pattern + a new delegation tool in `Supervisor.__init__` + a constructor parameter.

## Known incomplete / broken state (work in progress)

- `procesar` in both specialists reads `res["message"]` — the agent result key is `res["messages"]` (as `Supervisor.chat` uses), so delegation will raise `KeyError` until fixed.
- `supervisor.py` has no entry point (no model/agent instantiation or `chat()` call), an unused `from unittest import result`, and no `load_dotenv` import.
- System prompt strings are concatenated without separating spaces/periods.
