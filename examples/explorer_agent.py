from context_sdk import AgentContext
import time

ctx = AgentContext(api_key="agent_key_1")

seen_summary = None
query_handled = False

def on_change(data):
    time.sleep(2)
    global seen_summary, query_handled
    key, val = data["key"], data["value"]

    if key == "memx:query" and not query_handled:
        print(f"🔍 ExplorerAgent researching: {val}")
        ctx.set("memx:search_results:0", "LLaMA 2 is seeing adoption in healthcare companies")
        ctx.set("memx:thoughts:0", "Most OSS models require internal fine-tuning capacity")
        query_handled = True

    elif key == "memx:summary" and val != seen_summary:
        seen_summary = val
        ctx.set("memx:thoughts:1", "Consider adding hosted vs self-hosted trade-offs")
        print("🔄 ExplorerAgent added follow-up thoughts based on summary")

ctx.subscribe("memx:query", on_change)
ctx.subscribe("memx:summary", on_change)

while True:
    time.sleep(1)
