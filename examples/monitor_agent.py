from context_sdk import memxContext
import time

ctx = memxContext(api_key="agent_key_1")

def log(data):
    print(f"📡 Monitor saw: {data['key']} → {data['value']}")

for k in [
    "memx:query",
    "memx:context",
    "memx:search_results:0",
    "memx:summary",
    "memx:thoughts:0",
    "memx:thoughts:1"
]:
    ctx.subscribe(k, log)

while True:
    time.sleep(1)
