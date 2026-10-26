# NOVA

NOVA is a self-hosted, configuration-first AI companion runtime. The service owns stable interaction and safety boundaries; its behavior, persona, allowed users, and model failover order are declarative.

## Runtime model

```text
Telegram / HTTP -> Runtime -> Persona workspace -> Model failover chain
                                      |          Ollama -> Gemini -> Groq -> NVIDIA -> OpenRouter
                                      +-> policy, identity, instructions
```

The runtime tries providers in priority order and only fails over on retryable provider failures. Every request carries a correlation ID and returns the provider that answered it.

## Local setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,telegram]"
Copy-Item .env.example .env
nova
```

NOVA loads `config/nova.yaml` by default. Copy it before deploying and add only the provider keys needed for your selected chain.

## Configuration

- `config/nova.yaml` defines HTTP, Telegram policy, provider priorities, timeouts, and retry policy.
- `workspace/` supplies `SOUL.md`, `IDENTITY.md`, and `AGENTS.md`; it is mounted read-only by default in Docker.
- Provider API keys remain in environment variables, never YAML or Git.

## Verification

```powershell
ruff check .
pytest
```