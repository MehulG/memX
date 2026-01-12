# Looping Critique Demo (A -> B -> C -> B)

Agent B is reactive to two keys, so it runs twice in one flow:
**A (research) -> B (critique) -> C (final) -> B (post-review)**.
No locks. No orchestrator. Pure state + pub/sub.

## Keys
- `loop:research`
- `loop:critique_v1`
- `loop:final`
- `loop:critique_v2`

## Setup (Poetry)
```bash
cd examples/plan-coordniate
cp .env.example .env          # fill in GOOGLE_API_KEY and any overrides
poetry install                # project deps + virtualenv
poetry run python -m pip install memx-sdk langchain-google-genai
```

Agents auto-load `.env` from this folder via `dotenv`, so no manual exports needed.

Optional overrides:
- `MEMX_DEMO_MODEL_RESEARCH` / `MEMX_DEMO_MODEL_CRITIC` / `MEMX_DEMO_MODEL_SYNTHESIZER` - model names

## Run (four terminals)
```bash
cd examples/plan-coordniate

# T1
poetry run python agent_critic.py

# T2
poetry run python agent_synthesizer.py

# T3
poetry run python monitor.py

# T4 (trigger)
poetry run python agent_researcher.py
```

What you'll see:
- A writes `loop:research`
- B fires on research and writes `loop:critique_v1`
- C fires on `loop:critique_v1` and writes `loop:final`
- B fires again on `loop:final` and writes `loop:critique_v2`
- Monitor shows the chain in real time

Agents stay running so you can rerun `agent_researcher.py` to kick off another loop; Ctrl+C to stop any process.
