from context_sdk import AgentContext
import time

ctx = AgentContext(api_key="agent_key_1")

def on_update(data):
    print("🔥 Update received:", data)

ctx.subscribe("agent:goal", on_update)

ctx.set("agent:goal", "go to kitchen")
time.sleep(1)
ctx.set("agent:goal", "go to hallway")
time.sleep(3)
