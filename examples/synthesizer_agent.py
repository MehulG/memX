from context_sdk import AgentContext
import time

ctx = AgentContext(api_key="agent_key_1")

search_seen = False
thoughts_seen = []
count = 0
def maybe_summarize(data, num):
    global count
    if search_seen and len(thoughts_seen) >= 1:
        if count == 0:
            summary = (
                "Open-source LLMs are being adopted by enterprises. Many require internal fine-tuning capacity."
            )
            ctx.set("memx:summary", summary)
            print("📝 SynthesizerAgent wrote a summary.")

        elif count >= 1:
            summary = (
                "Open-source LLMs are being adopted by enterprises. Many require internal fine-tuning capacity. Hosted vs self-hosted deployment trade-offs are also emerging."
            )
            print("📝 SynthesizerAgent wrote the final summary.")
            print(summary)

def on_search(data):
    global search_seen
    search_seen = True
    maybe_summarize(data, 1)

def on_thought(data):
    global thoughts_seen
    val = data["value"]
    if val not in thoughts_seen:
        thoughts_seen.append(val)
    maybe_summarize(val, 2)
    global count 
    count += 1

ctx.subscribe("memx:search_results:0", on_search)
ctx.subscribe("memx:thoughts:0", on_thought)
ctx.subscribe("memx:thoughts:1", on_thought)

while True:
    time.sleep(1)
