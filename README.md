# 🧠 memX: Shared Memory for Multi-Agent LLM Systems

**memX** is an open-source real-time shared memory layer designed for agent-based systems powered by LLMs. It enables **coordination-first workflows** via:

* ⚡ Real-time CRDT-style state sync
* 📐 JSON Schema enforcement for data sanity
* 🔐 API-key-based access control
* 📣 Pub/Sub updates for reactive agents

---

## 🔍 What Problem Does memX Solve?

Modern multi-agent setups—whether using LangGraph, Autogen, or custom orchestration—lack a reliable way to **share evolving context** (state, goals, thoughts) between agents. memX provides a simple and secure memory layer that agents can read/write from in real-time — no message-passing or controller required.

---

## 🤖 Example: Collaborative LLM Agents Using memX

Three autonomous agents solving a research task, fully decentralized:

| Agent              | Behavior                                             |
| ------------------ | ---------------------------------------------------- |
| `QueryAgent`       | Seeds the research question + background context     |
| `ExplorerAgent`    | Adds search results + working notes                  |
| `SynthesizerAgent` | Summarizes the shared context into final insights    |
| `MonitorAgent`     | Logs real-time evolution of memory for observability |

> All communication flows through **shared keys** in memX — not through chat or a controller.

![memX agent demo](./assets/example.gif)

---

## 🚀 Features at a Glance

✅ Real-time memory sync (WebSocket)
📬 Pub/Sub updates on change
📐 Per-key JSON Schema validation
🔐 Fine-grained ACLs via API keys
🐍 Python SDK (`memx-sdk`) for easy integration
🐳 Docker-compatible for local hosting or cloud deployment

---

## ⚡ Quickstart

### 1. Install the SDK

```bash
pip install memx-sdk
```

### 2. Generate an API Key

Visit: [mem-x.vercel.com](https://mem-x.vercel.com)
Generate scoped API keys with just a few clicks.

### 3. Use in Python

```python
from context_sdk import memxContext

ctx = memxContext(api_key="your_api_key")

ctx.set_schema("agent:goal", {
  "type": "object",
  "properties": {"x": {"type": "number"}, "y": {"type": "number"}},
  "required": ["x", "y"]
})

ctx.set("agent:goal", {"x": 1, "y": 7})
print(ctx.get("agent:goal"))
```

---

## 🧰 Running memX Locally

### Option 1: Dev Server

```bash
uvicorn main:app --reload
```

### Option 2: Docker

```bash
docker-compose up --build
```

Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔑 API Key Management

### Hosted

1. Log in at [mem-x.vercel.com](https://mem-x.vercel.com)
2. Generate API keys with scoped access control

### Local Config

Edit `config/acl.json` to define access scopes:

```json
{
  "agent_key_1": ["agent:*"],
  "planner_key": ["agent:goal"]
}
```

---

## 📐 Define Schemas (Optional but Recommended)

Set schema for a key via API:

```bash
POST /schema
Headers: x-api-key: your_key
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

Or via SDK:

```python
ctx.set_schema("agent:state", schema_dict)
```

---

## 🗂 Project Structure

```
core/       # FastAPI + WebSocket backend
sdk/        # Python SDK (pip installable)
config/     # Access control & schemas
examples/   # LLM agent integration demos
```

---

## 🌐 Use Cases

* LangGraph / Autogen workflows with shared memory
* Autonomous research or planning agents
* IoT / robotics with real-time state coordination
* Any multi-agent system needing structured memory

---

## 📣 Join Us

memX is built for developers pushing the frontier of multi-agent systems.
Explore the SDK, try out agent demos, and contribute!

---
