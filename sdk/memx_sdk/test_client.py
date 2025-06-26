from memx_sdk import memxContext
import time

schema = {
    "type": "object",
    "properties": { "x": { "type": "number" }, "y": { "type": "number" } },
    "required": ["x", "y"]
}
ctx = memxContext(api_key="agent_key_1")


ctx.set_schema("agent:state", schema)
print(ctx.get_schema("agent:state"))
# ctx.delete_schema("agent:state")


def on_update(data):
    print("🔥 Update received:", data)

ctx.subscribe("agent:goal", on_update)

ctx.set("agent:goal", "go to kitchen")
time.sleep(1)
ctx.set("agent:goal", "go to hallway")
time.sleep(3)


