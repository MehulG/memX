# 🧠 memx-sdk

A Python client for [memX](https://github.com/MehulG/memX) — a real-time shared memory layer for multi-agent LLM systems.

Built for fast, schema-validated coordination between autonomous agents. Supports JSON key/value operations, schema enforcement, and pub/sub via WebSocket.

---

## 🚀 Features

- 🔑 Authenticate via API keys
- 📥 Get/set JSON values by key
- 📐 Define and validate key schemas
- 🔄 Real-time memory sync via WebSocket
- 🔔 Pub/sub for key-level updates

---

## 📦 Installation

```bash
pip install memx-sdk
```

## 🧪 Usage Example

Log in to [dashboard](https://mem-x.vercel.app) and create api keys with relevent scopes.

```python
from memx_sdk import Client

client = Client(api_key="your-api-key")

# Define schema
client.set_schema("agent:goal", {
    "type": "object",
    "properties": { "x": { "type": "number" }, "y": { "type": "number" } },
    "required": ["x", "y"]
})

# Set a value
client.set("agent:goal", {"x": 3, "y": 5})

# Get a value
value = client.get("agent:goal")
print(value)

# Subscribe to updates
def on_update(data):
    print("Updated:", data)

client.subscribe("agent:goal", callback=on_update)
```

## 🛠️ Requirements
- Python 3.7+
- httpx
- websockets

## 📄 License
MIT

## 🧠 Learn More
- Dashboard: https://mem-x.vercel.app
- Project: [memX README](https://github.com/MehulG/memX)