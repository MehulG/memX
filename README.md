# 🧠 memX

memX is an open source real-time shared memory layer for multi-agent LLM systems.

Built for coordination-first workflows with:
- JSON Schema enforcement
- API-key-based ACLs
- Pub/Sub updates

---

## 🎬 Example: Multi-Agent LLMs Using memX Shared Memory

💡 **Three autonomous LLM agents collaborate on a research task** using memX — no chat, no controller, just shared memory.

🧠 Each agent reads/writes to shared keys:

| Agent            | What it does                                     |
|------------------|--------------------------------------------------|
| `QueryAgent`     | Seeds the research question + background context |
| `ExplorerAgent`  | Adds search results + working thoughts           |
| `SynthesizerAgent` | Summarizes shared context into a final insight |
| `MonitorAgent`   | Logs how memory evolves in real time             |

> 💡 All communication happens *only* through shared keys in memX.

![memX agent demo](./assets/example.gif)

## 🚀 Features

* 🔄 Real-time context sync (WebSocket)
* 📬 Pub/sub updates on key change
* 📐 JSON Schema validation (per key)
* 🔐 API key-based access control
* 🐍 Python SDK (`memx-sdk`) for easy integration
* 🐳 Docker-compatible self-hosting

---

## 📦 Quickstart

### ▶️ Install SDK

```bash
pip install memx-sdk
```

### 💡 Usage Example

```python
from context_sdk import memxContext
ctx = memxContext(api_key="api_key")
ctx.set_schema("agent:goal", {
    "type": "object",
    "properties": {
      "x": { "type": "number" },
      "y": { "type": "number" }
    },
    "required": ["x", "y"]
  })
get1 = ctx.get("agent:goal")
print(get1)
ctx.set("agent:goal", {"x":1, "y":7})

```
---

## ⚙️ Run the Server

### Option 1: Local Dev

```bash
uvicorn main:app --reload
```

### Option 2: Docker

```bash
docker-compose up --build
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

---

## 🔑 Adding API Keys

Edit `config/acl.json`:

```json
{
  "agent_key_1": ["agent:*"],
  "planner_key": ["agent:goal"]
}
```

---

## 📐 Setting Schemas

```bash
POST /schema
Headers: x-api-key
Body:
{
  "key": "agent:state",
  "schema": {
    "type": "object",
    "properties": {"x": {"type": "number"}, "y": {"type": "number"}},
    "required": ["x", "y"]
  }
}
```

Or dynamically via SDK:

```python
ctx.set_schema("agent:state", schema_dict)
```

---

## 📁 Project Structure

```
core/       # FastAPI + WebSocket backend
sdk/        # Python SDK (installable)
config/     # Contains acl.json, (optionally schemas.json)
examples/   # Agent examples
```
